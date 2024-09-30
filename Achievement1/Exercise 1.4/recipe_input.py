import pickle


def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = 'Easy'
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = 'Medium'
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty = 'Intermediate'
    else:
        difficulty = 'Hard'
    return difficulty


def take_recipe():
    recipe_name = input("Enter the recipe name: ")
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    ingredients = input("Enter the ingredients (separate by commas): ").split(", ")


    difficulty = calc_difficulty(cooking_time, ingredients)


    recipe = {
        'Recipe Name': recipe_name,
        'Cooking Time': cooking_time,
        'Ingredients': ingredients,
        'Difficulty': difficulty
    }

    return recipe


filename = input("Enter a filename with your recipes: ")

try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File not found. Creating a new file.")
    data = {'recipes_list': [], 'all_ingredients': []}
except:
    print("Unexpected error. Creating a new file. ")
    data = {'recipes_list': [], 'all_ingredients': []}
else:
    file.close()
finally:
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']


num_recipes = int(input("How many recipes would you like to enter? "))


for i in range(num_recipes):
    recipe = take_recipe()
    recipes_list.append(recipe)  


    for ingredient in recipe['Ingredients']:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)


data['recipes_list'] = recipes_list
data['all_ingredients'] = all_ingredients


with open(filename, 'wb') as file:
    pickle.dump(data, file)

print("Recipe file has been updated!")