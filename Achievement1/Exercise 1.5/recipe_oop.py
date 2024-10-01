class Recipe:
    all_ingredients = []

    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = None

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time
        self.difficulty = self.calculate_difficulty()

    def get_cooking_time(self):
        return self.cooking_time

    def add_ingredients(self, *args):
        for ingredient in args:
            self.ingredients.append(ingredient)
            self.difficulty = self.calculate_difficulty()
        self.update_all_ingredients()

    def get_ingredients(self):
        return self.ingredients

    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            return "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            return "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            return "Intermediate"
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            return "Hard"

    def get_difficulty(self):
        self.calculate_difficulty()
        return self.difficulty

    def search_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            return True
        else:
            return False

    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)

    def __str__(self):
        return f"Recipe: {self.name}\nIngredients: {', '.join(self.ingredients)}\nCooking Time: {self.cooking_time} minutes\nDifficulty: {self.get_difficulty()}\n--------------------------"

    def recipe_search(data, search_term):
        print('\nRecipes that include ingredient',
              search_term, '\n' + 40 * '-')
        for recipe in data:
            if recipe.search_ingredient(search_term):
                print(recipe.name)

tea = Recipe("Tea")
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
tea.set_cooking_time(5)


coffee = Recipe("Coffee")
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
coffee.set_cooking_time(5)


cake = Recipe("Cake")
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
cake.set_cooking_time(50)


banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
banana_smoothie.set_cooking_time(5)



print(tea)
print(coffee)
print(cake)
print(banana_smoothie)

recipes_list = [tea, coffee, cake, banana_smoothie]
Recipe.recipe_search(recipes_list, 'Water')
Recipe.recipe_search(recipes_list, 'Sugar')
Recipe.recipe_search(recipes_list, 'Bananas')