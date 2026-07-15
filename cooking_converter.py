# cooking_converter.py

# Convert everything to a baseline unit (milliliters for volume, grams for weight)
VOLUME_TO_ML = {
    "teaspoon": 4.92892, "teaspoons": 4.92892, "tsp": 4.92892, "tsp.": 4.92892,
    "tablespoon": 14.7868, "tablespoons": 14.7868, "tbsp": 14.7868, "tbsp.": 14.7868,
    "fluid ounce": 29.5735, "fluid ounces": 29.5735, "fl oz": 29.5735, "fl. oz.": 29.5735,
    "cup": 236.588, "cups": 236.588, "c": 236.588, "c.": 236.588,
    "pint": 473.176, "pints": 473.176, "pt": 473.176,
    "quart": 946.353, "quarts": 946.353, "qt": 946.353,
    "gallon": 3785.41, "gallons": 3785.41, "gal": 3785.41,
    "milliliter": 1.0, "milliliters": 1.0, "ml": 1.0, "mL": 1.0,
    "liter": 1000.0, "liters": 1000.0, "l": 1000.0, "L": 1000.0
}

WEIGHT_TO_G = {
    "ounce": 28.3495, "ounces": 28.3495, "oz": 28.3495, "oz.": 28.3495,
    "pound": 453.592, "pounds": 453.592, "lb": 453.592, "lbs": 453.592, "lbs.": 453.592,
    "gram": 1.0, "grams": 1.0, "g": 1.0,
    "kilogram": 1000.0, "kilograms": 1000.0, "kg": 1000.0
}

def clean_unit(unit_str: str) -> str:
    """Standardizes unit strings to lowercase and strips trailing periods."""
    if not unit_str:
        return ""
    return unit_str.strip().lower().rstrip('.')

def convert_to_highest_unit(amount: float, unit: str) -> tuple[float, str]:
    """
    Normalizes a measurement and scales it up to the largest sensible 
    culinary unit if the amount crosses the threshold.
    """
    unit_clean = clean_unit(unit)
    
    # 1. Handle Volume Conversions
    if unit_clean in VOLUME_TO_ML:
        total_ml = amount * VOLUME_TO_ML[unit_clean]
        
        # Check from largest to smallest unit threshold
        if total_ml >= VOLUME_TO_ML["gallon"] * 0.95:  # Close enough to a gallon
            return total_ml / VOLUME_TO_ML["gallon"], "gallons"
        if total_ml >= VOLUME_TO_ML["quart"] * 0.95:
            return total_ml / VOLUME_TO_ML["quart"], "quarts"
        if total_ml >= VOLUME_TO_ML["cup"] * 0.95:
            return total_ml / VOLUME_TO_ML["cup"], "cups"
        if total_ml >= VOLUME_TO_ML["tablespoon"] * 2.95: # 3+ tbsp becomes cups/tbsp
            return total_ml / VOLUME_TO_ML["tablespoon"], "tablespoons"
        return total_ml / VOLUME_TO_ML["teaspoon"], "teaspoons"

    # 2. Handle Weight Conversions
    if unit_clean in WEIGHT_TO_G:
        total_g = amount * WEIGHT_TO_G[unit_clean]
        
        if total_g >= WEIGHT_TO_G["pound"] * 0.95:
            return total_g / WEIGHT_TO_G["pound"], "pounds"
        if total_g >= WEIGHT_TO_G["ounce"] * 0.95:
            return total_g / WEIGHT_TO_G["ounce"], "ounces"
        return total_g, "grams"

    # 3. Fallback for non-convertible items (e.g., "cloves", "whole", "pinch")
    return amount, unit
