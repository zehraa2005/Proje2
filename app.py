import sqlite3


def find_recipe(meal_type, user_input):
    # Veritabanı isminin doğruluğundan emin oluyoruz
    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()

    # Kullanıcı girdisini parçala ve küçük harfe çevir
    # "Egg, Milk" -> ['egg', 'milk']
    search_terms = [term.strip().lower() for term in user_input.split(',')]

    print(f"\n🔍 Searching for '{meal_type}' recipes containing: {', '.join(search_terms)}...\n")

    # Kategori Seçimi
    target_categories = []
    if meal_type == "1":
        target_categories = ['Breakfast']
    elif meal_type == "2":
        target_categories = ['Chicken', 'Beef', 'Seafood', 'Pasta', 'Lamb', 'Pork', 'Vegetarian', 'Side', 'Starter',
                             'Goat', 'Vegan']
    elif meal_type == "3":
        target_categories = ['Dessert']
    else:
        target_categories = ['Breakfast', 'Chicken', 'Beef', 'Dessert', 'Pasta']

    # SQL Sorgusu Hazırlama
    placeholders = ', '.join(['?'] * len(target_categories))

    # Püf Nokta: 'lower(ingredients)' kullanarak büyük/küçük harf sorununu çözüyoruz.
    sql_query = f"SELECT meal_name, category, ingredients, instructions FROM recipes WHERE category IN ({placeholders})"

    params = list(target_categories)

    for term in search_terms:
        sql_query += " AND lower(ingredients) LIKE ?"
        params.append(f'%{term}%')

    cursor.execute(sql_query, params)
    results = cursor.fetchall()

    if results:
        print(f"🎉 Great! Found {len(results)} recipes matching ALL your criteria:\n")
        for i, meal in enumerate(results, 1):
            name, cat, ings, instructions = meal
            print(f"{i}. {name} [{cat}]")
            print(f"   🛒 Ingredients: {ings[:100]}...")
            print(f"   👨‍🍳 Instructions: {instructions[:150]}...")
            print("-" * 50)
    else:
        print("😔 Sorry, no recipes found containing ALL those ingredients together.")
        print("Tip: Try searching for fewer ingredients (e.g., just 'egg').")

    conn.close()


def main():
    print("========================================")
    print("   🍳 SMART KITCHEN ASSISTANT (v3.0) 🍳")
    print("========================================")

    # SİSTEM KONTROLÜ (Veritabanı Dolu mu?)
    try:
        conn = sqlite3.connect("recipes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM recipes")
        count = cursor.fetchone()[0]
        print(f"📊 SYSTEM STATUS: {count} recipes loaded in database.")
        conn.close()
    except:
        print("❌ ERROR: Database 'recipes.db' not found. Please run 'database_setup.py' first.")
        return

    while True:
        print("\n--- MENU ---")
        print("1. Breakfast")
        print("2. Main Course (Dinner/Lunch)")
        print("3. Dessert")
        print("Q. Quit")

        choice = input("Select Meal Type (1-3): ").strip().lower()

        if choice == 'q':
            print("Goodbye! 👋")
            break

        if choice not in ['1', '2', '3']:
            print("❌ Invalid selection.")
            continue

        ingredient = input("Enter ingredients (separated by comma): ").strip()

        if len(ingredient) > 1:
            find_recipe(choice, ingredient)
        else:
            print("❌ Please enter valid ingredients.")


if __name__ == "__main__":
    main()