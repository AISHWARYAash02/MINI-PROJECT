# predict_nutrition_text_local.py

import pandas as pd
import difflib
import os

# ---------- 1️⃣ Paths ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "nutrition_data.csv")

# ---------- 2️⃣ Load and preprocess nutrition data ----------
nutrition_df = pd.read_csv(CSV_PATH)
nutrition_df['food_name_normalized'] = (
    nutrition_df['food_name']
    .astype(str)
    .str.lower()
    .str.replace(" ", "_")
    .str.strip()
)

normalized_names = nutrition_df['food_name_normalized'].tolist()

# ---------- 3️⃣ Utility ----------
def normalize_name(s: str) -> str:
    """Normalize food name for matching."""
    return str(s).lower().replace(" ", "_").strip()

# <<< ADD THE SAME KEY-MAPPING LOGIC HERE
def get_nutrition_from_series(food_series):
    """Cleans up the nutrition series from pandas to have consistent keys."""
    raw_nutrition = food_series.to_dict()
    
    key_map = {
        'calories (kcal)': 'calories',
        'protein (g)': 'protein',
        'carbohydrates (g)': 'carbs',
        'fat (g)': 'fat'
    }
    
    cleaned_nutrition = {}
    for csv_key, value in raw_nutrition.items():
        normalized_csv_key = csv_key.lower().strip()
        if normalized_csv_key in key_map:
            cleaned_nutrition[key_map[normalized_csv_key]] = value
            
    return cleaned_nutrition

# ---------- 4️⃣ Nutrition lookup ----------
def nutrition_from_text(food_name_input):
    """Find nutrition info from a food name entered as text."""
    query = normalize_name(food_name_input)
    
    # Exact match
    match = nutrition_df[nutrition_df['food_name_normalized'] == query]
    
    # Try fuzzy matching if exact not found
    if match.empty:
        candidates = difflib.get_close_matches(query, normalized_names, n=1, cutoff=0.6)
        if candidates:
            best = candidates[0]
            match = nutrition_df[nutrition_df['food_name_normalized'] == best]
        else:
            return None

    if not match.empty:
        # <<< USE THE NEW CLEANING FUNCTION BEFORE RETURNING
        return get_nutrition_from_series(match.iloc[0])
        
    return None

# ---------- 5️⃣ Example usage ----------
if __name__ == "__main__":
    test_input = "banana"
    result = nutrition_from_text(test_input)
    if result:
        print(f"✅ Nutrition for '{test_input}':\n", result)
    else:
        print(f"❌ No match found for '{test_input}'.")
