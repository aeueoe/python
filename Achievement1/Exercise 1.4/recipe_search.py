import pickle


def display_recipe(recipe):
    print("\nRecipe Details:")
    print(f"Recipe Name: {recipe['Recipe Name']}")
    print(f"Cooking Time: {recipe['Cooking Time']} minutes")
    print(f"Ingredients: {', '.join(recipe['Ingredients'])}")
    print(f"Difficulty: {recipe['Difficulty']}")


def search_ingredient(data):
  
    print("\nAvailable Ingredients:")
    for i, ingredient in enumerate(data['all_ingredients']):
        print(f"{i}. {ingredient}")

    try:
       
        index = int(input("Enter the number of the ingredient you want to search for: "))
        ingredient_searched = data['all_ingredients'][index]
    except (IndexError, ValueError):
        print("Invalid selection. Please enter a valid number.")
        return
    else:
        print(f"\nSearching for recipes with the ingredient: {ingredient_searched}")
   
        found = False
        for recipe in data['recipes_list']:
            if ingredient_searched in recipe['Ingredients']:
                display_recipe(recipe)
                found = True
        if not found:
            print("No recipes found with the selected ingredient.")


filename = input("Enter the binary file name: ")

try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    print(f"File {filename} not found.")
else:
    search_ingredient(data)