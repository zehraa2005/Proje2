import scrapy
import json


class MealSpider(scrapy.Spider):
    name = "meals"
    allowed_domains = ["www.themealdb.com"]

    # WE CHANGED THIS: Now fetching Breakfast, Dessert, and Main Course categories
    start_urls = [
        "https://www.themealdb.com/api/json/v1/1/filter.php?c=Breakfast",
        "https://www.themealdb.com/api/json/v1/1/filter.php?c=Dessert",
        "https://www.themealdb.com/api/json/v1/1/filter.php?c=Chicken",
        "https://www.themealdb.com/api/json/v1/1/filter.php?c=Beef",
        "https://www.themealdb.com/api/json/v1/1/filter.php?c=Pasta",
        "https://www.themealdb.com/api/json/v1/1/filter.php?c=Seafood",
        "https://www.themealdb.com/api/json/v1/1/filter.php?c=Vegetarian"
    ]

    def parse(self, response):
        """
        Parses the JSON response containing the list of meals for a category.
        """
        data = response.json()

        if 'meals' in data and data['meals']:
            print(f"--- Found {len(data['meals'])} recipes in this category ---")

            for meal in data['meals']:
                meal_id = meal['idMeal']
                # Request details for each meal
                details_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
                yield scrapy.Request(url=details_url, callback=self.parse_details)
        else:
            print("--- No meals found! ---")

    def parse_details(self, response):
        """
        Parses the detailed information of a specific meal.
        """
        data = response.json()
        meal_data = data['meals'][0]

        meal_name = meal_data.get('strMeal')
        instructions = meal_data.get('strInstructions')
        category = meal_data.get('strCategory')
        tags = meal_data.get('strTags')

        # Collecting ingredients into a single list
        ingredients = []
        for i in range(1, 21):
            ing_name = meal_data.get(f'strIngredient{i}')
            measure = meal_data.get(f'strMeasure{i}')

            if ing_name and ing_name.strip():
                full_ing = f"{ing_name.strip()}"
                if measure and measure.strip():
                    full_ing += f" ({measure.strip()})"
                ingredients.append(full_ing)

        print(f"--> SAVED: {meal_name} ({category})")

        yield {
            'meal_name': meal_name,
            'category': category,
            'tags': tags,
            'ingredients': ingredients,
            'instructions': instructions,
            'image_url': meal_data.get('strMealThumb'),
            'source_url': response.url
        }