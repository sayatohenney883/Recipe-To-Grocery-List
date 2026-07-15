import requests

class SpoonacularService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.spoonacular.com/recipes"

    def search_recipes(self, query: str, number: int = 30) -> list:
        """Searches for recipes by name, including image URLs."""
        url = f"{self.base_url}/complexSearch"
        params = {
            "apiKey": self.api_key,
            "query": query,
            "number": number
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            # Extract title, id, and image from results
            results = response.json().get("results", [])
            cleaned_recipes = []
            for r in results:
                cleaned_recipes.append({
                    "id": r.get("id"),
                    "title": r.get("title"),
                    "image": r.get("image")  # <--- Grab the image URL here
                })
            return cleaned_recipes
        except requests.RequestException as e:
            print(f"\n[Error] Failed to fetch recipes: {e}")
            return []

    def get_recipe_ingredients(self, recipe_id: int) -> list:
        """Fetches detailed ingredient information for a specific recipe."""
        url = f"{self.base_url}/{recipe_id}/information"
        params = {"apiKey": self.api_key, "includeNutrition": "false"}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            # Extract just the clean ingredient data we need
            extended_ingredients = response.json().get("extendedIngredients", [])
            ingredients = []
            for ing in extended_ingredients:
                ingredients.append({
                    "name": ing.get("nameClean") or ing.get("name"),
                    "amount": ing.get("amount"),
                    "unit": ing.get("unit")
                })
            return ingredients
        except requests.RequestException as e:
            print(f"\n[Error] Failed to fetch recipe details: {e}")
            return []

