import random
import google.generativeai as genai
import json
from datetime import datetime

# Configure Gemini API (replace with your API key)
GEMINI_API_KEY = "AIzaSyDzb_AnhJU3MyMT1rW5U3IXI4ZZrxhfX08"  # Replace with your actual key
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")  # Use Gemini 1.5 Pro or another model

def generate_meal_combo(budget, dietary, spice_level, time_of_day):
    """
    Generate mock meal combo options (meal + beverage) for a Sri Lankan university cafeteria.
    Uses Gemini API for dynamic suggestions, with mock data as fallback.
    Parameters:
        budget (int): Maximum budget in Rs. (e.g., 300).
        dietary (str): Dietary preference (e.g., 'Vegetarian', 'Vegan', 'Non-Veg', 'Any').
        spice_level (str): Spice preference (e.g., 'Mild', 'Medium', 'Spicy', 'Any').
        time_of_day (str): Current time in 'HH:MM' format (e.g., '15:06').
    Returns:
        list: List of dictionaries with meal combo details for one day.
    """
    # Mock data for meals
    meals = {
        "Any": [
            {"name": "Rice & Curry", "price": 200, "dietary": ["Vegetarian"], "spice": "Medium", "prep_time": 10},
            {"name": "Biriyani", "price": 250, "dietary": ["Non-Veg"], "spice": "Spicy", "prep_time": 15},
            {"name": "Fried Rice", "price": 220, "dietary": ["Non-Veg", "Vegetarian"], "spice": "Spicy", "prep_time": 12},
            {"name": "Noodles", "price": 180, "dietary": ["Vegetarian"], "spice": "Medium", "prep_time": 8},
            {"name": "String Hoppers", "price": 150, "dietary": ["Vegetarian"], "spice": "Mild", "prep_time": 10},
            {"name": "Hoppers", "price": 120, "dietary": ["Vegetarian"], "spice": "Mild", "prep_time": 8},
            {"name": "Kottu", "price": 230, "dietary": ["Non-Veg"], "spice": "Spicy", "prep_time": 15}
        ],
        "Vegetarian": [
            {"name": "Rice & Curry", "price": 200, "dietary": ["Vegetarian"], "spice": "Medium", "prep_time": 10},
            {"name": "Fried Rice", "price": 220, "dietary": ["Vegetarian"], "spice": "Spicy", "prep_time": 12},
            {"name": "Noodles", "price": 180, "dietary": ["Vegetarian"], "spice": "Medium", "prep_time": 8},
            {"name": "String Hoppers", "price": 150, "dietary": ["Vegetarian"], "spice": "Mild", "prep_time": 10},
            {"name": "Hoppers", "price": 120, "dietary": ["Vegetarian"], "spice": "Mild", "prep_time": 8}
        ],
        "Vegan": [
            {"name": "Vegetable Noodles", "price": 180, "dietary": ["Vegan"], "spice": "Medium", "prep_time": 8},
            {"name": "Coconut Milk Curry", "price": 190, "dietary": ["Vegan"], "spice": "Mild", "prep_time": 10}
        ],
        "Non-Veg": [
            {"name": "Biriyani", "price": 250, "dietary": ["Non-Veg"], "spice": "Spicy", "prep_time": 15},
            {"name": "Fried Rice", "price": 220, "dietary": ["Non-Veg"], "spice": "Spicy", "prep_time": 12},
            {"name": "Kottu", "price": 230, "dietary": ["Non-Veg"], "spice": "Spicy", "prep_time": 15}
        ]
    }

    # Mock data for beverages
    beverages = {
        "Any": [
            {"name": "Nest Tea", "price": 60, "dietary": ["Any"], "prep_time": 5},
            {"name": "Nest Cafe", "price": 80, "dietary": ["Any"], "prep_time": 5},
            {"name": "Fresh Juice", "price": 120, "dietary": ["Vegan"], "prep_time": 7},
            {"name": "Soft Drinks", "price": 100, "dietary": ["Any"], "prep_time": 2},
            {"name": "Milk Packets", "price": 50, "dietary": ["Vegetarian"], "prep_time": 2}
        ],
        "Vegetarian": [
            {"name": "Nest Tea", "price": 60, "dietary": ["Vegetarian"], "prep_time": 5},
            {"name": "Fresh Juice", "price": 120, "dietary": ["Vegetarian"], "prep_time": 7},
            {"name": "Milk Packets", "price": 50, "dietary": ["Vegetarian"], "prep_time": 2}
        ],
        "Vegan": [
            {"name": "Fresh Juice", "price": 120, "dietary": ["Vegan"], "prep_time": 7}
        ],
        "Non-Veg": [
            {"name": "Nest Tea", "price": 60, "dietary": ["Any"], "prep_time": 5},
            {"name": "Nest Cafe", "price": 80, "dietary": ["Any"], "prep_time": 5},
            {"name": "Soft Drinks", "price": 100, "dietary": ["Any"], "prep_time": 2}
        ]
    }

    # Parse time of day for meal appropriateness
    try:
        hour = int(time_of_day.split(":")[0])
    except:
        hour = 15  # Default to 3 PM if time parsing fails
    breakfast_time = 6 <= hour < 10
    lunch_time = 10 <= hour < 15
    dinner_time = 15 <= hour < 20

    # Select meals based on dietary, spice, and time
    dietary = dietary if dietary in meals else "Any"
    spice_level = spice_level if spice_level in ["Mild", "Medium", "Spicy", "Any"] else "Any"
    selected_meals = [
        m for m in meals[dietary]
        if (spice_level == "Any" or m["spice"] == spice_level) and
           (
               (breakfast_time and m["name"] in ["Hoppers", "String Hoppers"]) or
               (lunch_time and m["name"] in ["Rice & Curry", "Biriyani", "Fried Rice", "Noodles"]) or
               (dinner_time and m["name"] in ["Kottu", "Fried Rice", "Noodles"]) or
               True  # Allow all if time not restrictive
           )
    ]

    # Select beverages based on dietary
    selected_beverages = beverages[dietary]

    # Try Gemini API for dynamic combo
    prompt = (
        f"Generate a meal combo (one meal + one beverage) for a Sri Lankan university cafeteria, "
        f"under Rs. {budget}, for a {dietary} diet with {spice_level} flavor, suitable for {time_of_day}. "
        f"Return a JSON object with fields: meal_name, beverage_name, total_price, prep_time."
    )
    try:
        response = model.generate_content(prompt)
        combo = json.loads(response.text.strip("```json\n").strip("```"))
        options = [{
            "day": "Today",
            "meal_name": combo["meal_name"],
            "beverage_name": combo["beverage_name"],
            "total_price": combo["total_price"],
            "prep_time": combo["prep_time"]
        }]
        return options
    except Exception as e:
        # Fallback to mock data
        pass

    # Generate fallback combo using mock data
    selected_meals = random.sample(selected_meals, min(1, len(selected_meals)))
    selected_beverages = random.sample(selected_beverages, min(1, len(selected_beverages)))
    options = []
    for meal, beverage in zip(selected_meals, selected_beverages):
        total_price = meal["price"] + beverage["price"]
        if total_price <= budget:
            options.append({
                "day": "Today",
                "meal_name": meal["name"],
                "beverage_name": beverage["name"],
                "total_price": total_price,
                "prep_time": meal["prep_time"] + beverage["prep_time"]
            })
            break  # Single combo for simplicity

    # Default combo if none fit
    if not options:
        options = [{
            "day": "Today",
            "meal_name": "Rice & Curry",
            "beverage_name": "Nest Tea",
            "total_price": 260,
            "prep_time": 15
        }]

    return options