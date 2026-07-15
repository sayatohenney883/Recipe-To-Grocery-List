from spoonacular_service import SpoonacularService
from shopping_list import ShoppingListManager
import webbrowser

API_KEY = "f40a269ff8144faeaed5bdf43e975993"

def main():

    api = SpoonacularService(API_KEY)
    manager = ShoppingListManager()

    while True:
        print("\n=== CENTRAL MENU ===")
        print("1. Search & Add Recipe")
        print("2. View Planned Recipes")
        print("3. Remove a Recipe")
        print("4. View Shopping List")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            query = input("\nWhat food item or dish are you looking for? ")
            recipes = api.search_recipes(query)

            if not recipes:
                print("No recipes found. Try a different search term.")
                continue

            # Clean list: just show the names and numbers, no ugly unclickable URLs
            print(f"\nResults matching '{query}':")
            for idx, r in enumerate(recipes, 1):
                print(f"{idx}. {r['title']}")

            try:
                sel = int(input("\nSelect a recipe number to view ingredients (or 0 to cancel): "))
                if sel == 0 or sel > len(recipes):
                    continue
                
                chosen_recipe = recipes[sel - 1]
                r_id = chosen_recipe["id"]
                r_title = chosen_recipe["title"]
                r_image = chosen_recipe.get("image")

                # Image logic triggers ONLY after selection
                if r_image:
                    print(f"\nAttempting to open recipe image in your web browser...")
                    opened = webbrowser.open(r_image)
                    
                    import os
                    if not opened or "CODESPACES" in os.environ or "REPLIT_SLUG" in os.environ:
                        print("\n[System] Automated browser opening is unavailable in this environment.")
                        print("Scan this QR code with your phone to view the recipe image:")
                        import qrcode
                        qr = qrcode.QRCode(version=1, box_size=1, border=1)
                        qr.add_data(r_image)
                        qr.make(fit=True)
                        qr.print_ascii(invert=True) 

                # Fetch detailed ingredients from the API
                print(f"\nFetching ingredients for '{r_title}'...")
                ingredients = api.get_recipe_ingredients(r_id)
                
                if not ingredients:
                    print("Could not retrieve ingredients for this recipe.")
                    continue

                # Display the ingredients to the user
                print(f"\n--- Ingredients for {r_title} ---")
                for ing in ingredients:
                    print(f"• {ing['amount']} {ing['unit']} {ing['name']}")
                print("-" * 30)

                # Prompt confirmation
                confirm = input(f"\nWould you like to add these ingredients to your shopping list? (y/n): ").lower()
                if confirm == 'y':
                    manager.add_recipe(r_id, r_title, ingredients)
                else:
                    print("Returned to menu without adding.")
            except ValueError:
                print("Invalid input. Returning to menu.")

        elif choice == "2":
            recipes = manager.get_all_recipes()
            print("\n--- Current Meal Plan ---")
            if not recipes:
                print("No recipes added yet!")
            for r_id, title in recipes.items():
                print(f"- {title} (ID: {r_id})")

        elif choice == "3":
            recipes = manager.get_all_recipes()
            print("\n--- Remove a Recipe ---")
            if not recipes:
                print("Your meal plan is currently empty.")
                continue

            # Convert to a list so the user can just type a simple number instead of a huge API ID
            recipe_list = list(recipes.items())
            for idx, (r_id, title) in enumerate(recipe_list, 1):
                print(f"{idx}. {title}")

            try:
                sel = int(input("\nSelect the number of the recipe to remove (or 0 to cancel): "))
                if sel == 0 or sel > len(recipe_list):
                    continue
                
                target_id, target_title = recipe_list[sel - 1]
                confirm = input(f"Are you sure you want to remove '{target_title}' and its ingredients? (y/n): ").lower()
                
                if confirm == 'y':
                    manager.delete_recipe(target_id)
                else:
                    print("Removal canceled.")
            except ValueError:
                print("Invalid input. Returning to menu.")

        elif choice == "4":
            import math
            shop_list = manager.get_shopping_list()
            print("\n--- Your Aggregated Shopping List ---")
            if not shop_list:
                print("Your list is empty. Add some recipes first!")
            for item in shop_list:
                amt = item['amount']
                
                # If it's a fractional teaspoon/tablespoon (like 0.5), keep it clean.
                # Otherwise, round up to the next clean whole number.
                if 0 < amt <= 0.5:
                    final_amt = 0.5
                else:
                    final_amt = math.ceil(amt)
                
                print(f"• {item['name']}: {final_amt} {item['unit']}")
        elif choice == "5":
            print("\nHappy cooking! Goodbye.")
            break
        else:
            print("Invalid selection. Try again.")

if __name__ == "__main__":
    main()

