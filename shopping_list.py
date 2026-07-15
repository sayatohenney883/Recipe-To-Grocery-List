# shopping_list.py
from cooking_converter import VOLUME_TO_ML, WEIGHT_TO_G, clean_unit, convert_to_highest_unit

class ShoppingListManager:
    def __init__(self):
        self.selected_recipes = {}     # { recipe_id: recipe_title }
        self.recipe_ingredients = {}   # { recipe_id: [list_of_ingredients] }
        self.master_ingredients = {}   # { ingredient_name: {unit: str, amount_in_base: float, type: str} }

    def add_recipe(self, recipe_id: int, title: str, ingredients: list):
        if recipe_id in self.selected_recipes:
            print(f"\n'{title}' is already added!")
            return

        self.selected_recipes[recipe_id] = title
        self.recipe_ingredients[recipe_id] = ingredients
        self._rebuild_master_list()
        print(f"\nSuccessfully added ingredients from '{title}'!")

    def delete_recipe(self, recipe_id: int):
        if recipe_id in self.selected_recipes:
            title = self.selected_recipes.pop(recipe_id)
            self.recipe_ingredients.pop(recipe_id, None)
            self._rebuild_master_list()
            print(f"\nRemoved '{title}' from your plan.")
        else:
            print("\n[Error] Recipe ID not found in your current plan.")

    def _rebuild_master_list(self):
        """Recalculates totals by converting items into shared baseline values."""
        self.master_ingredients.clear()
        
        for ingredients_list in self.recipe_ingredients.values():
            for ing in ingredients_list:
                name = ing["name"].lower()
                amount = float(ing["amount"])
                unit = clean_unit(ing["unit"])

                # Determine tracking system type
                if unit in VOLUME_TO_ML:
                    base_amount = amount * VOLUME_TO_ML[unit]
                    unit_type = "volume"
                    base_unit = "ml"
                elif unit in WEIGHT_TO_G:
                    base_amount = amount * WEIGHT_TO_G[unit]
                    unit_type = "weight"
                    base_unit = "g"
                else:
                    base_amount = amount
                    unit_type = "discrete"
                    base_unit = unit

                # Aggregate matching systems under the ingredient name
                if name in self.master_ingredients:
                    # Only add mathematically if they share the same physical type (volume vs weight)
                    if self.master_ingredients[name]["type"] == unit_type:
                        self.master_ingredients[name]["amount_in_base"] += base_amount
                    else:
                        # Fallback if recipe uses mixed types (e.g. 1 cup onions vs 50 grams onions)
                        # Append a unique identifier slot to prevent erasing data
                        alt_name = f"{name} ({unit_type})"
                        if alt_name in self.master_ingredients:
                            self.master_ingredients[alt_name]["amount_in_base"] += base_amount
                        else:
                            self.master_ingredients[alt_name] = {"amount_in_base": base_amount, "base_unit": base_unit, "type": unit_type}
                else:
                    self.master_ingredients[name] = {"amount_in_base": base_amount, "base_unit": base_unit, "type": unit_type}

    def get_all_recipes(self) -> dict:
        return self.selected_recipes

    def get_shopping_list(self) -> list:
        """Processes the internal base values back out into clear, human-readable kitchen scales."""
        readable_list = []
        for name, data in self.master_ingredients.items():
            if data["type"] in ["volume", "weight"]:
                # Convert the large consolidated base numbers up into clean cups, quarts, or pounds
                final_amount, final_unit = convert_to_highest_unit(data["amount_in_base"], data["base_unit"])
                readable_list.append({"name": name, "amount": final_amount, "unit": final_unit})
            else:
                # Discrete items like 'cloves' or 'whole' bypass conversions
                readable_list.append({"name": name, "amount": data["amount_in_base"], "unit": data["base_unit"]})
        return readable_list

