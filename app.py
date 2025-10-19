# app.py (Gradient Glow & Scanlines Design)

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
    background-size: 100% 10px;
    pointer-events: none;
    z-index: 1;
}

.main .block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 0;
    padding-right: 0;
    max-width: 100%;
    position: relative;
    z-index: 2;
}

.title-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100vw;
    padding: 2rem 0;
    box-sizing: border-box;
    margin-left: calc(-50vw + 50%);
    margin-right: calc(-50vw + 50%);
}

/* Gradient Glow Title */
.glow-title {
    font-size: 7vw;
    font-weight: 800;
    background: linear-gradient(90deg, #00F0FF, #FFFFFF, #00F0FF);
    background-size: 200% auto;
    color: #000; /* Set text color to black for the gradient to show through */
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    filter: drop-shadow(0 0 10px #00F0FF) drop-shadow(0 0 20px #00F0FF);
    animation: shine 3s linear infinite;
    line-height: 1.1;
    white-space: nowrap;
    letter-spacing: 0.05em;
}

@keyframes shine {
    to { background-position: 200% center; }
}

/* Glowing Button */
div.stButton > button:first-child {
    background-color: transparent;
    border: 2px solid #00F0FF;
    color: #FFFFFF;
    font-size: 1.5rem;
    font-weight: 700;
    padding: 0.5em 2em;
    border-radius: 10px;
    box-shadow: 0 0 10px #00F0FF, 0 0 20px #00F0FF;
    transition: all 0.3s ease-in-out;
}

div.stButton > button:hover {
    background-color: #00F0FF;
    color: #0E1117;
    box-shadow: 0 0 20px #00F0FF, 0 0 30px #00F0FF, 0 0 40px #00F0FF;
    transform: scale(1.05);
}

/* Hide sidebar and footer */
[data-testid="stSidebar"] { display: none; }
[data-testid="stFooter"] { display: none; }
</style>
""", unsafe_allow_html=True)


# --- Page Content ---

st.markdown("<div class='title-container'><h1 class='glow-title'>SMART NUTRITION AI</h1></div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Predict", use_container_width=True):
        st.switch_page("pages/1_Home.py")
