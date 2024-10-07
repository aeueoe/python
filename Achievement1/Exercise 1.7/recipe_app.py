from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqlconnector://cf-python:1703@localhost/myrecipes')


Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Recipe(Base):
    __tablename__ = 'final_recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"Recipe(id={self.id}, name='{self.name}', difficulty='{self.difficulty}')"

    def __str__(self):
        return f"Recipe {self.id}: {self.name}\nIngredients: {self.ingredients}\nCooking Time: {self.cooking_time} minutes\nDifficulty: {self.difficulty}"

    def calculate_difficulty(self):
        difficulty = None
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            difficulty = 'Easy'
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            difficulty = 'Medium'
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            difficulty = 'Intermediate'
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            difficulty = 'Hard'

        print("Difficulty of recipe: " + difficulty)
        self.difficulty = difficulty

    def return_ingredients_as_list(self):
        if self.ingredients == '':
            return []
        else:
            return self.ingredients.split(', ')

Base.metadata.create_all(engine)


def create_recipe():
    session = Session()
    print("\nCreate a New Recipe")
    print("---------------------")
    name = input("Enter recipe name: ")
    while len(name) > 50:
        print("Name should not be more than 50 characters.")
        name = input("Enter recipe name: ")

    ingredients = []
    num_ingredients = int(input("Enter number of ingredients: "))
    for i in range(num_ingredients):
        ingredient = input(f"Enter ingredient {i+1}: ")
        ingredients.append(ingredient)
    ingredients_str = ', '.join(ingredients)

    cooking_time = input("Enter cooking time in minutes: ")
    while not cooking_time.isnumeric():
        print("Cooking time should be a number.")
        cooking_time = input("Enter cooking time in minutes: ")

    recipe_entry = Recipe(name=name, ingredients=ingredients_str, cooking_time=int(cooking_time))
    recipe_entry.calculate_difficulty()
    session.add(recipe_entry)
    session.commit()
    print("\n Recipe Added Succesfully!")
session.close()


def view_all_recipes():
    session = Session()
    print("\nView All Recipes")
    print("----------------")
    recipes = session.query(Recipe).all()
    if not recipes:
        print("No recipes found.")
        return
    for recipe in recipes:
        print(recipe)
        print("\n")



def search_by_ingredients():
    # Check if any recipes exist on our database, and continue only if there are any
    recipes_count = session.query(Recipe).count()
    if recipes_count == 0:
        print("\n There are currently no recipes in the database!!")
        # Notify and return to main menu if no recipes exist in database
        return None
    else:
        # Get ingredients list from all recipe objects
        recipes_list = session.query(Recipe).all()
        recipes_ingredients = [recipe.ingredients for recipe in recipes_list]

        # Separate and add (non repetitively) to all_ingredients each ingredient from ingrediets list on each recipe object
        all_ingredients = []
        for recipe_ingredient in recipes_ingredients:
            recipe_ingredients = recipe_ingredient.split(", ")
            for ingredient in recipe_ingredients:
                if ingredient not in all_ingredients:
                    all_ingredients.append(ingredient)

        # Print a list of all ingredients in all_ingredients list
        print("\n List of ingredients on the current recipes present on database: " + "\n" + 45*"-")
        count = 1
        for ingredient in all_ingredients:
            print(count, "- ", ingredient)
            count = count + 1

        # Store user input of searched ingredient on search_ingredient variable
        search_num = input(
            '\nEnter the corresponding numbers of the ingredients you want to search (Separate each numbers by space inbetween):   ')
        search_num = search_num.split(" ")

        search_ingredients = []
        for n in search_num:
            index = int(n) - 1
            if int(n) <= count:
                ingredient = all_ingredients[index]
                search_ingredients.append(ingredient)

        # Set conditions list for conditions for each ingredient to be searched for
        conditions = []
        for ingredient in search_ingredients:
            like_term = "%" + ingredient + "%"
            conditions.append(Recipe.ingredients.like(like_term))

        # Display list of recipes with searched ingredients in ingredients list
        searched_recipes = session.query(Recipe).filter(*conditions).all()
        print("Recipes with ingredients you searched are:" + "\n" + 45*"-")
        for recipe in searched_recipes:
            print("- " + recipe.name)
            print("\n")


# Edit recipe from recipes list
def edit_recipe():
    # Check if any recipes exist on our database, and continue only if there are any
    recipes_count = session.query(Recipe).count()
    if recipes_count == 0:
        print("\n There are currently no recipes to edit in the database!!")
        return None
    else:
        recipes_list = session.query(Recipe).all()
        print("\n Choose from the following recipes available to edit:" + "\n" + 50*"-")
        recipe_ID_available = []
        for recipe in recipes_list:
            print("ID", recipe.id, "-", recipe.name)
            recipe_ID_available.append(recipe.id)
        id_picked = int(
            input("\nEnter the corresponding id number of the recipe you want to edit:  "))

        if id_picked in recipe_ID_available:
            recipe_to_edit = session.query(Recipe).filter(
                Recipe.id == id_picked).one()
            print(
                "Choose the corresponding number of the recipe attribute you want to edit: ")
            print("\n1 - Recipe Name: " + recipe_to_edit.name + "\n2 - Recipe Cooking time: " +
                  str(recipe_to_edit.cooking_time) + "\n3 - Ingredients: " + str(recipe_to_edit.ingredients))
            chosen_attribute = int(input('\nEnter your number here:   '))

            if chosen_attribute == 1 or chosen_attribute == 2 or chosen_attribute == 3:
                if chosen_attribute == 1:
                    name_input = str(
                        input('Enter a new name for the recipe (LETTERS ONLY, max of 50 char.):   '))
                    if len(name_input) < 51 and name_input.isalpha():
                        recipe_to_edit.name = name_input
                        print("\n You have changed recipe name to",
                              recipe_to_edit.name)
                    else:
                        print(
                            "\nYou have entered words either greater than 50 in length or included numbers or symbols in your name! Try again or Ctrl+C to exit")
                        edit_recipe()

                elif chosen_attribute == 2:
                    cooking_time_input = input(
                        'Enter the total cooking time (INTEGER NUMBERS ONLY):   ')
                    if cooking_time_input.isnumeric():
                        cooking_time = int(cooking_time_input)
                        recipe_to_edit.cooking_time = cooking_time
                        print("\n You have changed recipe cooking time to",
                              recipe_to_edit.cooking_time)
                    else:
                        print(
                            "\nYou have not entered cooking time correctly, please enter cooking time in whole integer numbers or Ctrl+C to exit")
                        edit_recipe()

                elif chosen_attribute == 3:
                    ingredients = []
                    n = int(input(
                        'Enter the number ingredients for this recipe (max ingredient no. 255):   '))
                    if n > 255:
                        print(
                            "\n Maximum number of ingredients is 255, please try again!!")
                        edit_recipe()
                    else:
                        print(
                            "\n Enter The ingredients for the recipe: " + "\n" + 40*"-")
                        # Use for loop to fill ingredients list to avoid string representation
                        for i in range(0, n):
                            # Format on ingredients
                            ingredient = input(' - ')
                            ingredients.append(ingredient)
                    ingredients = ", ".join(ingredients)
                    recipe_to_edit.ingredients = ingredients
                    print("\n You have changed recipe ingredients to ", ingredients)

                # Recalculate the difficulty using the object 'recipe_to_edit' calculate_difficulty() method
                recipe_to_edit.calculate_difficulty()

                # Commit the change edited to the database
                session.commit()

            else:
                print(
                    "\n The number you have chosen is not in the attributes list, try again!")
                edit_recipe()

        else:
            print("The id you picked is not available on the list for edit!")
            edit_recipe()




def delete_recipe():
    session = Session()
    print("\nDelete a Recipe")
    print("----------------")
    if not session.query(Recipe).count():
        print("No recipes found.")
        return

    results = session.query(Recipe.id, Recipe.name).all()
    for id, name in results:
        print(f"{id}. {name}")

    recipe_id = input("Enter id of recipe to delete: ")
    while not recipe_id.isnumeric():
        print("Invalid id.")
        recipe_id = input("Enter id of recipe to delete: ")

    recipe_to_delete = session.get(Recipe, int(recipe_id))  
    if recipe_to_delete is None:
        print("Recipe not found.")
        return

    confirm = input("Are you sure you want to delete this recipe? (yes/no): ")
    if confirm.lower() == 'yes':
        session.delete(recipe_to_delete)
        session.commit()
        print("Recipe deleted.")
    else:
        print("Deletion cancelled.")
    session.close()



def main_menu():
    choice = None
    while not choice == 'quit':
        print("\n     Main Menu" + "\n" + 40*"=")
        print("What would you like to do? Pick a choice!")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for a recipe by ingredient")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            create_recipe()
        elif choice == '2':
            view_all_recipes()
        elif choice == '3':
            search_by_ingredients()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")


main_menu()
print("Goodbye!")