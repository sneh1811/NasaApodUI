import streamlit as st
import requests
import time
import random

st.set_page_config(page_title="NASA Astronomy Picture of the Day AI", page_icon="🌌", layout="centered")

# CSS Animations & Styles
st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .title {
        text-align: center;
        font-size: 3em;
        letter-spacing: 2px;
        color: #f39c12;
        text-shadow: 0 0 15px rgba(243, 156, 18, 0.8);
    }
    body { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); }
    .main { backdrop-filter: blur(20px); padding: 20px; border-radius: 15px; box-shadow: 0 0 20px rgba(0, 0, 0, 0.6); }
    .float-btn { position: fixed; bottom: 20px; right: 20px; background: #f39c12; color: white; padding: 10px 20px; border-radius: 50px; cursor: pointer; text-align: center; font-weight: bold; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4); }
    .cosmic-text {
        text-align: center;
        font-size: 1.5em;
        color: #f39c12;
        text-shadow: 0 0 10px rgba(243, 156, 18, 0.8);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Title with Animation
st.markdown("""<div class='title'>🚀 NASA APOD AI 9000™</div>""", unsafe_allow_html=True)
st.markdown("""<div class='cosmic-text'>Uncover the Cosmic Mysteries with AI + NASA 🌌</div>""", unsafe_allow_html=True)

# Random NASA Facts
nasa_facts = [
    "Did you know? NASA's Voyager 1 is the farthest human-made object from Earth!",
    "Cosmic Fact: A day on Venus is longer than its year!",
    "Trivia: Saturn has 82 moons... and counting!",
    "Fact: The Sun is actually white, not yellow!"
]

# Query Input
query = st.text_input("What cosmic mystery would you like to uncover today? 🔍")

if st.button("🚀 Ignite Cosmic Discovery") or (query and st.session_state.get("enter_pressed", True)):
    if query:
        loading_placeholder = st.empty()
        progress_bar = st.progress(0)
        st.write(f"💡 {random.choice(nasa_facts)}")
        toggle = True
        for percent in range(95):
            time.sleep(0.2)
            progress_bar.progress(percent + 1)
            if percent % 30 == 0:
                toggle = not toggle
                loading_placeholder.text("🚀 Scanning the Universe..." if toggle else "Fetching cosmic content... 🌌")
        
        try:
            response = requests.post("https://nasaapod.onrender.com/get_nasa_apod", json={"query": query})
            data = response.json()

            if "error" in data:
                st.error(data["error"])
            else:
                progress_bar.empty()
                loading_placeholder.empty()
                st.subheader(data["title"])
                st.write(f"**Date:** {data["date"]}")
                st.write(data["explanation"])

                if data["media_type"] == "image":
                    st.image(data["image_url"], caption="NASA Astronomy Picture of the Day", use_container_width=True)
                elif data["media_type"] == "video":
                    st.video(data["video_url"])
        except Exception as e:
            st.error("Something went wrong. Please try again later.")
    else:
        st.warning("Please enter a query.")
