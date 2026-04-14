import streamlit as st
import streamlit.components.v1 as components

# 1. This makes the app look right on a phone screen
st.set_page_config(
    page_title="Shuttle Dispatch Pro",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. This CSS hides the Streamlit "header" and "footer" 
# so your uncle thinks it's a native app, not a website.
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {margin: 0; padding: 0;}
    iframe {border-radius: 15px;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# 3. This reads your 2,000 lines of code and "injects" them
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 4. This displays your app
components.html(html_content, height=1000, scrolling=True)