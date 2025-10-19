# predict_food_nutrition_local.py
import os
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array

# ---------- 1️⃣ Paths ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "unified_food_model.keras")
CLASS_NAMES_PATH = os.path.join(BASE_DIR, "models", "class_names.txt")
NUTRITION_CSV = os.path.join(BASE_DIR, "nutrition_data.csv")

# ---------- 2️⃣ Load nutrition CSV ----------
nutrition_df = pd.read_csv(NUTRITION_CSV)

# Normalize the food names in the CSV for easier matching
# This assumes your food column is named 'food_name'. If not, change it here.
nutrition_df['food_name_normalized'] = (
    nutrition_df['food_name'].astype(str)
    .str.lower()
    .str.replace(" ", "_") # Matching folder naming convention
    .str.strip()
)

def normalize_name(name: str) -> str:
    """Normalize a food name to match the CSV format."""
    return str(name).lower().replace(" ", "_").strip()

# <<< FINAL FIX: A robust function to get and clean nutrition data
# In predict_food_nutrition_local.py, replace the existing get_nutrition function with this one:

# In predict_food_nutrition_local.py

def get_nutrition(food_name):
    """Find nutrition info and map the keys to what the app expects."""
    normalized = normalize_name(food_name)
    
    # Try for an exact match first
    match = nutrition_df[nutrition_df['food_name_normalized'] == normalized]
    if match.empty:
        # If no exact match, try a partial match
        match = nutrition_df[nutrition_df['food_name_normalized'].str.contains(normalized, na=False)]

    if match.empty:
        return None # No food found in CSV

    # Get the nutrition data as a dictionary
    raw_nutrition = match.iloc[0].to_dict()

    # <<< FINAL, CORRECTED KEY MAP
    key_map = {
        'calories (kcal)': 'calories',
        'protein (g)': 'protein',
        'carbohydrates (g)': 'carbs', # <<< THIS LINE IS THE FIX
        'fat (g)': 'fat'
    }
    
    # Create a new dictionary with the cleaned keys
    cleaned_nutrition = {}
    for csv_key, value in raw_nutrition.items():
        # Normalize the key from the CSV to find a match in our map
        normalized_csv_key = csv_key.lower().strip()
        if normalized_csv_key in key_map:
            cleaned_nutrition[key_map[normalized_csv_key]] = value
            
    return cleaned_nutrition

# ---------- 3️⃣ Load the unified model ----------
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model not found: {MODEL_PATH}. Please run the training script first.")

model = load_model(MODEL_PATH)

if not os.path.exists(CLASS_NAMES_PATH):
    raise FileNotFoundError(f"❌ Class names file not found: {CLASS_NAMES_PATH}. Please run the training script first.")

with open(CLASS_NAMES_PATH, "r") as f:
    class_labels = [line.strip() for line in f.readlines()]

# ---------- 4️⃣ Image preprocessing ----------
def preprocess_image(img_path, target_size=(224, 224)):
    img = load_img(img_path, target_size=target_size)
    arr = img_to_array(img).astype("float32") / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr

# ---------- 5️⃣ Predict food ----------
def predict_food(image_path):
    img_arr = preprocess_image(image_path)
    preds = model.predict(img_arr, verbose=0)
    idx = int(np.argmax(preds[0]))
    conf = float(preds[0][idx])
    food = class_labels[idx]
    return food, conf

# ---------- 6️⃣ Full prediction with nutrition ----------
def enhanced_predict_food(image_path, min_conf=0.70):
    food, conf = predict_food(image_path)
    
    if food.lower() == "non_food":
        return {"error": "🚫 This doesn't appear to be a food item. Please upload a clear food image."}
    
    if conf < min_conf:
        return {"error": f"🤔 I'm not confident enough to identify this as '{food}' (Confidence: {conf:.2%}). Please try a clearer image."}

    nutrition = get_nutrition(food)
    if not nutrition:
        return {"error": f" Please upload a valid food image"}

    result = {"food_name": food, "confidence": f"{conf:.2%}", "nutrition": nutrition}
    return result

# ---------- 7️⃣ Example usage ----------
if __name__ == "__main__":
    test_img_path = os.path.join(BASE_DIR, "test_images", "mango.jpeg") 
    if not os.path.exists(test_img_path):
        print(f"⚠️ Test image not found at: {test_img_path}")
        print("Please create a 'test_images' folder and add a food image (e.g., mango.jpeg) to it.")
    else:
        print(f"--- Testing with image: {test_img_path} ---")
        res = enhanced_predict_food(test_img_path)
        print(res)
