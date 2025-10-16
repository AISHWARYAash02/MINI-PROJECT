# pages/4_Diet_Recommendation.py

import streamlit as st

# Local modules
from diet_recommendation_local import recommend_diet

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

/* Style for our custom recommendation box */
.glowing-recommendation-box {
    background-color: #1A1F2E;
    border: 1px solid #00F0FF;
    border-radius: 15px;
    padding: 1.5em;
    margin-top: 2em;
    box-shadow: 0 0 10px #00F0FF, 0 0 20px #00F0FF;
}

.glowing-recommendation-box h3 {
    color: #00F0FF;
    margin-top: 0;
    margin-bottom: 1em;
    font-size: 1.1rem;
    border-bottom: 1px solid rgba(0, 240, 255, 0.3);
    padding-bottom: 0.5em;
}

.glowing-recommendation-box .metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.8em;
}

.glowing-recommendation-box .metric-label {
    color: #B0B0B0;
    font-size: 0.9rem;
}

.glowing-recommendation-box .metric-value {
    color: #FFFFFF;
    font-size: 1.2rem;
    font-weight: 600;
}

/* Style for the new suggestion box */
.glowing-suggestion-box {
    background-color: #1A2E2A; /* A slightly different color */
    border: 1px solid #00FF7F; /* A different glow color (green) */
    border-radius: 15px;
    padding: 1.5em;
    margin-top: 1.5em;
    box-shadow: 0 0 10px #00FF7F, 0 0 20px #00FF7F;
}

.glowing-suggestion-box h3 {
    color: #00FF7F; /* Green title */
    margin-top: 0;
    margin-bottom: 1em;
    font-size: 1.1rem;
    border-bottom: 1px solid rgba(0, 255, 127, 0.3);
    padding-bottom: 0.5em;
}

.glowing-suggestion-box p {
    color: #E0E0E0;
    line-height: 1.6;
}

/* Style for input fields and selectboxes */
.stSelectbox > div > div > select, .stNumberInput > div > div > input {
    background-color: #1A1F2E;
    border: 1px solid #00F0FF;
    color: #FFFFFF;
    border-radius: 10px;
}

/* Home Button */
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

st.title("📋 Personalized Diet Recommendation")
st.markdown("---")

# Input section
st.subheader("Enter Your Profile Details")

# Create columns for a better layout
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=1, max_value=120, value=25, key="age")
    gender = st.selectbox("Gender", ["male", "female"], key="gender")
    weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, key="weight")

with col2:
    height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=175.0, key="height")
    activity_level = st.selectbox("Activity Level", 
                                  ["Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"], key="activity")
    goal = st.selectbox("Goal", ["Maintain weight", "Weight loss", "Weight gain"], key="goal")

if st.button("Recommend Diet", use_container_width=True, key="recommend_btn"):
    with st.spinner('🧮 Calculating your recommendations...'):
        result = recommend_diet(age, gender, weight, height, activity_level, goal)
        bmi_status = result['bmi_status']
        
        # --- Suggestions based on BMI ---
        # <<< FIX: Removed the extra opening brace '{' from the line below
        suggestions = {
            "Underweight": "Try adding more nutritious meals with healthy fats, proteins, and whole grains. Include light strength exercises and stay consistent. A dietitian can help you plan balanced meals.",
            "Normal weight": "Keep up your balanced diet, regular activity, and good sleep. Stay consistent with what works for you.",
            "Overweight": "Focus on balanced meals with more fruits, veggies, and lean proteins. Reduce sugary foods and stay active with daily walks or workouts.",
            "Obese": "Start with small lifestyle changes — balanced meals, gentle exercise, and plenty of rest. A healthcare expert can help create a plan that fits your goals."
        }
        
        suggestion_text = suggestions.get(bmi_status, "Maintain a balanced lifestyle and consult a professional for personalized advice.")

        # --- Build the HTML for the recommendation box ---
        daily_calories = result['calories']
        protein = result['protein_g']
        carbs = result['carbs_g']
        fat = result['fat_g']
        bmi = result['bmi']

        recommendation_html = f"""
        <div class="glowing-recommendation-box">
            <h3>✅ Your Personalized Diet Recommendation</h3>
            <div class="metric-row">
                <span class="metric-label">Daily Calories</span>
                <span class="metric-value">{daily_calories} kcal</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Protein</span>
                <span class="metric-value">{protein} g</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Carbs</span>
                <span class="metric-value">{carbs} g</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Fat</span>
                <span class="metric-value">{fat} g</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">BMI</span>
                <span class="metric-value">{bmi} ({bmi_status})</span>
            </div>
        </div>
        """
        st.markdown(recommendation_html, unsafe_allow_html=True)

        # --- Build the HTML for the new suggestion box ---
        suggestion_html = f"""
        <div class="glowing-suggestion-box">
            <h3>💡 Suggestions for You</h3>
            <p>{suggestion_text}</p>
        </div>
        """
        st.markdown(suggestion_html, unsafe_allow_html=True)

st.markdown("---")

# Home Button at the bottom
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🏠 Back to Home", use_container_width=True, key="home_btn"):
        st.switch_page("pages/1_Home.py")
