import sqlite3
import json
import os

# 1. DATABASE CONNECTION
# Creates a database file named 'recipes.db' (if it doesn't exist).
db_name = "recipes.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

print(f"--- Connected to Database: {db_name} ---")

# 2. TABLE CREATION (Schema Design)
# We use 'IF NOT EXISTS' to avoid errors if the table already exists.
create_table_query = """
                     CREATE TABLE IF NOT EXISTS recipes \
                     ( \
                         id \
                         INTEGER \
                         PRIMARY \
                         KEY \
                         AUTOINCREMENT, \
                         meal_name \
                         TEXT, \
                         category \
                         TEXT, \
                         tags \
                         TEXT, \
                         ingredients \
                         TEXT, \
                         instructions \
                         TEXT, \
                         image_url \
                         TEXT, \
                         source_url \
                         TEXT
                     ) \
                     """
cursor.execute(create_table_query)
print("--- Table Created (recipes) ---")

# 3. READING DATA FROM JSON FILE
json_file = "recipes.json"

if os.path.exists(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    print(f"--- {len(data)} recipes read from JSON file ---")

    # 4. INSERTING DATA INTO DATABASE
    # Iterate through each recipe and add it to the database.
    inserted_count = 0
    for item in data:
        # First, check if this meal already exists in the database (to prevent duplicates)
        cursor.execute("SELECT id FROM recipes WHERE meal_name = ?", (item['meal_name'],))
        existing_meal = cursor.fetchone()

        if existing_meal is None:
            # Convert ingredient list to string (SQLite does not store lists directly)
            # Example: ['Egg', 'Milk'] -> "Egg, Milk"
            ingredients_str = ", ".join(item['ingredients'])

            cursor.execute("""
                           INSERT INTO recipes (meal_name, category, tags, ingredients, instructions, image_url,
                                                source_url)
                           VALUES (?, ?, ?, ?, ?, ?, ?)
                           """, (
                               item['meal_name'],
                               item['category'],
                               item['tags'],
                               ingredients_str,
                               item['instructions'],
                               item['image_url'],
                               item['source_url']
                           ))
            inserted_count += 1
            print(f"Added: {item['meal_name']}")
        else:
            print(f"Already Exists (Skipped): {item['meal_name']}")

    # 5. SAVE AND CLOSE
    conn.commit()
    print(f"\n--- PROCESS COMPLETED! Total {inserted_count} new recipes added to database. ---")

else:
    print(f"ERROR: {json_file} not found! Please run the Scrapy code first.")

conn.close()