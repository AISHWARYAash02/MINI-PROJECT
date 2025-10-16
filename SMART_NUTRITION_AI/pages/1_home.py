# pages/1_Home.py

import streamlit as st

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
    background-size: 100% px;
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

/* Style for the buttons (boxes) */
button {
    background-color: #1A1F2E;
    border: 2px solid #00F0FF;
    border-radius: 15px;
    padding: 2em 1em;
    text-align: center;
    box-shadow: 0 0 15px #00F0FF, 0 0 25px #00F0FF;
    transition: all 0.3s ease-in-out;
    cursor: pointer;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-size: 1.2rem;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1.5;
    white-space: pre-line;
    min-height: 250px; /* <<< THIS IS THE ONLY ADDED LINE */
}

button:hover {
    transform: translateY(-10px);
    box-shadow: 0 0 25px #00F0FF, 0 0 35px #00F0FF, 0 0 45px #00F0FF;
    background-color: rgba(0, 240, 255, 0.1);
}

/* Hide sidebar and footer */
[data-testid="stSidebar"] { display: none; }
[data-testid="stFooter"] { display: none; }
</style>
""", unsafe_allow_html=True)

st.title("Choose an Objective")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📸\nImage Food Prediction", key="img_btn", help="Click to go to Image Prediction"):
        st.switch_page("pages/2_Image_Prediction.py")

with col2:
    if st.button("🔤\nText Food Nutrition", key="text_btn", help="Click to go to Text Nutrition"):
        st.switch_page("pages/3_Text_Nutrition.py")

with col3:
    if st.button("📋\nDiet Recommendation", key="diet_btn", help="Click to go to Diet Recommendation"):
        st.switch_page("pages/4_Diet_Recommendation.py")
