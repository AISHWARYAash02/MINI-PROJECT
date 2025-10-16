# pages/3_Text_Nutrition.py

import streamlit as st

# Local modules
from predict_nutrition_text_local import nutrition_from_text

# Define the glowing theme with CSS
st.markdown("""
<style>
/* Main body and font */
body {
    background-color: #0E1117;
    color: #FFFFFF;
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
}

/* Scanline overlay effect */
body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to bottom, transparent 50%, rgba(0, 240, 255, 0.03) 50%);
    background-size: 100% 10px;
    pointer-events: none;
    z-index: 1;
}

.main .block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 100%;
    position: relative;
    z-index: 2;
}

/* Page Title */
.stTitle {
    background: linear-gradient(90deg, #00F0FF, #FFFFFF, #00F0FF);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 5px #00F0FF);
    animation: shine 3s linear infinite;
}

@keyframes shine {
    to { background-position: 200% center; }
}

/* Style for our custom nutrition box */
.glowing-nutrition-box {
    background-color: #1A1F2E;
    border: 1px solid #00F0FF;
    border-radius: 15px;
    padding: 1.5em;
    margin-top: 2em;
    box-shadow: 0 0 10px #00F0FF, 0 0 20px #00F0FF;
}

.glowing-nutrition-box h3 {
    color: #00F0FF;
    margin-top: 0;
    margin-bottom: 1em;
    font-size: 1.1rem;
    border-bottom: 1px solid rgba(0, 240, 255, 0.3);
    padding-bottom: 0.5em;
}

.glowing-nutrition-box .metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.8em;
}

.glowing-nutrition-box .metric-label {
    color: #B0B0B0;
    font-size: 0.9rem;
}

.glowing-nutrition-box .metric-value {
    color: #FFFFFF;
    font-size: 1.2rem;
    font-weight: 600;
}

/* Style for the text input and button */
.stTextInput > div > div > input {
    background-color: #1A1F2E;
    border: 1px solid #00F0FF;
    color: #FFFFFF;
    border-radius: 10px;
}

div.stButton > button {
    background-color: transparent;
    border: 2px solid #00F0FF;
    color: #FFFFFF;
    font-weight: 700;
    padding: 0.5em 2em;
    border-radius: 10px;
    box-shadow: 0 0 10px #00F0FF, 0 0 20px #00F0FF;
    transition: all 0.3s ease-in-out;
    width: 100%;
}

div.stButton > button:hover {
    background-color: #00F0FF;
    color: #0E1117;
    box-shadow: 0 0 20px #00F0FF, 0 0 30px #00F0FF;
    transform: scale(1.05);
}

/* Hide sidebar and footer */
[data-testid="stSidebar"] { display: none; }
[data-testid="stFooter"] { display: none; }
</style>
""", unsafe_allow_html=True)

st.title("🔤 Text Food Nutrition")
st.markdown("---")

# Input section
food_name = st.text_input("Enter a food name (e.g., 1 cup of rice, apple)", placeholder="e.g., apple, 1 bowl of dal")

if st.button("Get Nutrition", use_container_width=True):
    if food_name.strip() != "":
        with st.spinner('🔍 Looking up nutrition...'):
            nutrition = nutrition_from_text(food_name)
            if nutrition:
                # Build the HTML for the nutrition box
                calories = nutrition.get('calories', 'N/A')
                protein = nutrition.get('protein', 'N/A')
                carbs = nutrition.get('carbs', 'N/A')
                fat = nutrition.get('fat', 'N/A')

                nutrition_html = f"""
                <div class="glowing-nutrition-box">
                    <h3>🥗 Nutrition Information for '{food_name}'</h3>
                    <div class="metric-row">
                        <span class="metric-label">Calories (kcal)</span>
                        <span class="metric-value">{calories}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">Protein (g)</span>
                        <span class="metric-value">{protein}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">Carbohydrates (g)</span>
                        <span class="metric-value">{carbs}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">Fat (g)</span>
                        <span class="metric-value">{fat}</span>
                    </div>
                </div>
                """
                st.markdown(nutrition_html, unsafe_allow_html=True)
            else:
                st.warning(f"❌ No nutrition info found for '{food_name}'. Try another name or check spelling.")
    else:
        st.warning("Please enter a food name.")

st.markdown("---")

# Home Button at the bottom
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("pages/1_Home.py")
