recipes_list = []
ingredients_list = []

n = int(input("How many recipes would you like to enter?: "))

def take_recipe():
    name = str(input("Enter the name of the recipe: "))
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    ingredients = (input("Enter the ingredients separated by commas: ").split(","))
    
    recipe = {
        'Name': name,
        'Cooking_Time': cooking_time,
        'Ingredients': ingredients
    }
    return recipe

for i in range(n):
    recipe = take_recipe()

    for ingredient in recipe['Ingredients']:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)

for recipe in recipes_list:
    if int(recipe['Cooking_Time']) < 10 and len(recipe['Ingredients']) < 4:
        difficulty = 'Easy'
    elif int(recipe['Cooking_Time']) < 10 and len(recipe['Ingredients']) >= 4:
        difficulty = 'Medium'
    elif int(recipe['Cooking_Time']) >= 10 and len(recipe['Ingredients']) < 4:
        difficulty = 'Intermediate'
    elif int(recipe['Cooking_Time']) >= 10 and len(recipe['Ingredients']) >= 4:
        difficulty = 'Hard'

    print("Recipe: ", recipe["Name"])
    print("Cooking Time (min): ", recipe["Cooking_Time"])
    print("Ingredients: ")
    for ingredient in recipe["Ingredients"]:
        print(ingredient)
    print("Difficulty Level: ", difficulty)

def all_ingredients():
    print("Ingredients Available Across All Recipes")
    print("________________________________________")
    ingredients_list.sort()
    for ingredient in ingredients_list:
        print(ingredient)

all_ingredients()