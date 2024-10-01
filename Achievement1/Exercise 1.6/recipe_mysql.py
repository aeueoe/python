import mysql.connector

conn = mysql.connector.connect(host="localhost", user="cf-python", passwd="1703")
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS recipes (
        id INT NOT NULL  PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50),
        ingredients VARCHAR(255),
        cooking_time INT,
        difficulty VARCHAR(20)
    )
    """
)

def calculate_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        return 'Easy'
    elif cooking_time < 10 and len(ingredients) >= 4:
        return 'Medium'
    elif cooking_time >= 10 and len(ingredients) < 4:
        return 'Intermediate'
    else:
        return 'Hard'

def create_recipe(conn, cursor):
    print("----------------------------")
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the cooking time (minutes): "))
    ingredients = input("Enter the ingredients: ").split(', ')
    difficulty = calculate_difficulty(cooking_time, ingredients)
    print(f"Difficulty level: {difficulty}")
    ingredients_str = ', '.join(ingredients)
    query = "INSERT INTO recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, ingredients_str, cooking_time, difficulty))
    conn.commit()
    print("Recipe saved into the database.")

def search_recipe(conn, cursor):
    cursor.execute("SELECT ingredients FROM recipes")
    results = cursor.fetchall()
    all_ingredients = []
    for row in results:
        ingredients = row[0].split(', ')
        all_ingredients.extend(ingredients)
    all_ingredients = list(set(all_ingredients))
    print("Available ingredients:")
    print("----------------------------")
    for i, ingredient in enumerate(all_ingredients):
        print(f"{i+1}. {ingredient}")
    search_ingredient = input("Enter the number of the ingredient to search for: ")
    search_ingredient = all_ingredients[int(search_ingredient) - 1]
    query = "SELECT * FROM recipes WHERE ingredients LIKE %s"
    cursor.execute(query, (f"%{search_ingredient}%",))
    results = cursor.fetchall()
    print("\nSearch Results:")
    print("----------------------------")
    for row in results:
        print("Name:", row[1])
        print("Ingredients:", row[2])
        print("Cooking Time:", row[3], "minutes")
        print("Difficulty:", row[4])
        print("------------------------")

def update_recipe(conn, cursor):
    # Get all recipes from database
    cursor.execute("SELECT * FROM recipes")
    results = cursor.fetchall()
    for i, row in enumerate(results):
        print(f"{i+1}. {row[1]}")
    recipe_id = int(input("\nEnter the number of the recipe you want to update: ")) - 1
    recipe_id = results[recipe_id][0]

    # Gets the recipes ID
    cursor.execute("SELECT name FROM recipes WHERE id = %s", (recipe_id,))
    result = cursor.fetchone()

    # handle errors
    if result is None:
        print("Recipe with ID %s does not exist." % recipe_id)
        return
    recipe_name = result[0]

    print("\n1. Name")
    print("2. Ingredients")
    print("3. Cooking Time")
    column_update = int(
        input(
            "\nEnter a number associated with what you want to update in %s."
            % recipe_name
        )
    )

    # Update the name of the recipe
    if column_update == 1:
        new_name = str(input("\nEnter the new name: ").title())
        query = "UPDATE recipes SET name = %s WHERE id = %s"
        cursor.execute(query, (new_name, recipe_id))
        conn.commit()
        print("Recipe updated successfully.")

    # Update the ingredients of the recipe
    elif column_update == 2:
        # Ask user for new ingredients
        ingredients_input = input("Enter the new ingredients for %s : " % recipe_name)

        # Capitalize each ingredient and remove any whitespace
        new_ingredients = ", ".join(
            [ingredient.strip().title() for ingredient in ingredients_input.split(",")]
        )

        # Update the ingredients in the database
        query = "UPDATE recipes SET ingredients = %s WHERE id = %s"
        cursor.execute(query, (new_ingredients, recipe_id))

        # Update the difficulty in the database
        cursor.execute("SELECT cooking_time FROM recipes WHERE id = %s", (recipe_id,))
        result = cursor.fetchone()
        current_cooking_time = result[0]
        # result is the current cooking time
        new_difficulty = calculate_difficulty(current_cooking_time, new_ingredients.split(', '))
        query = "UPDATE recipes SET difficulty = %s WHERE id = %s"
        cursor.execute(query, (new_difficulty, recipe_id))
        conn.commit()
        print("Recipe updated and difficulty calculated.")
    elif column_update == 3:
        # Ask user for new cooking time
        new_cooking_time = int(input("\nEnter the new cooking time (in minutes): "))
        query = "UPDATE recipes SET cooking_time = %s WHERE id = %s"
        cursor.execute(query, (new_cooking_time, recipe_id))

        # Update the difficulty in the database
        cursor.execute("SELECT ingredients FROM recipes WHERE id = %s", (recipe_id,))
        result = cursor.fetchone()
        current_ingredients = result[0]
        new_difficulty = calculate_difficulty(new_cooking_time, current_ingredients.split(', '))
        query = "UPDATE recipes SET difficulty = %s WHERE id = %s"
        cursor.execute(query, (new_difficulty, recipe_id))
        conn.commit()
        print("Recipe updated successfully.")
    else:
        print("Invalid input. Please try again.")

def delete_recipe(conn, cursor):
    cursor.execute("SELECT * FROM recipes")
    results = cursor.fetchall()
    for i, row in enumerate(results):
        print(f"{i+1}. {row[1]}")
    recipe_id = int(input("Enter the number of the recipe to delete: ")) - 1
    recipe_id = results[recipe_id][0]
    query = "DELETE FROM recipes WHERE id = %s"
    cursor.execute(query, (recipe_id,))
    conn.commit()

def view_all_recipes(conn, cursor):
    cursor.execute("SELECT * FROM recipes")
    results = cursor.fetchall()
    print("All Recipes:")
    print("----------------------------")
    for row in results:
        print(f"ID: {row[0]}, Name: {row[1]}, Ingredients: {row[2]}, Cooking Time: {row[3]} minutes, Difficulty: {row[4]}")

def main_menu(conn, cursor ):
    while True:
        print("\nMain Menu:")
        print("-------------")
        print("1. Create a recipe")
        print("2. Search for a recipe")
        print("3. Update a recipe")
        print("4. Delete a recipe")
        print("5. View all recipes")
        print("6. Quit")
        print("----------------------------")
        choice = input("Enter your choice: ")
        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == '5':
            view_all_recipes(conn, cursor)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

main_menu(conn, cursor)
print("Goodbye!")