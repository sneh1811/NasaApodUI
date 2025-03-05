import streamlit as st
import requests
import time
import random

st.set_page_config(page_title="NASA APOD AI 9000™", page_icon="🌌", layout="centered")
NASA_API_KEY = st.secrets["NASA_API_KEY"]
# Cosmic CSS Styles
st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    body { background: radial-gradient(circle, #0d1b2a 0%, #1b2735 50%, #090a0f 100%) !important; color: #ffffff; }
    .title {
        animation: fadeIn 2s ease-in-out;
        text-align: center;
        font-size: 3em;
        letter-spacing: 2px;
        color: #f39c12;
        text-shadow: 0 0 15px rgba(243, 156, 18, 0.8);
    }
    .cosmic-text {
        text-align: center;
        font-size: 1.5em;
        color: #f39c12;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🚀 NASA APOD AI 9000™</div>", unsafe_allow_html=True)
st.markdown("<div class='cosmic-text'>Uncover the Cosmic Mysteries with AI + NASA 🌌</div>", unsafe_allow_html=True)

nasa_facts = [
    "Did you know? NASA's Voyager 1 is the farthest human-made object from Earth!",
    "Cosmic Fact: A day on Venus is longer than its year!",
    "Trivia: Saturn has 82 moons... and counting!",
    "Fact: The Sun is actually white, not yellow!",
    "Voyager 1 is now over 14 billion miles away from Earth!",
    "Venus is the hottest planet in our solar system... not Mercury!",
    "A spoonful of neutron star would weigh about a billion tons!",
    "The Andromeda Galaxy will collide with the Milky Way... in 4 billion years!"
]

# Track which field was updated last
if "last_updated" not in st.session_state:
    st.session_state["last_updated"] = None


def set_last_updated(field):
    st.session_state["last_updated"] = field


# Input Fields with Callbacks
st.markdown("### Ask the Cosmos 🔍")
input_query = st.text_input(
    "Describe your Cosmic Curiosity", 
    key="input_query",
    on_change=set_last_updated,
    args=("input_query",)
)

st.markdown("### OR")


st.markdown("### Pick a Date to Discover the Cosmic Picture 🌌")
selected_date = st.date_input(
    "Pick a Date", 
    key="selected_date",
    on_change=set_last_updated,
    args=("selected_date",),
    value=None
)

# Set Query Based on Last Updated Field
query = ""
if st.session_state["last_updated"] == "input_query" and input_query:
    query = input_query
elif st.session_state["last_updated"] == "selected_date" and selected_date:
    query = selected_date.strftime("%Y-%m-%d")

if st.button("🚀 Ignite Cosmic Discovery"):
    if query:
        loading_placeholder = st.empty()
        st.write(f"💡 {random.choice(nasa_facts)}")
        progress_bar = st.progress(0)

        for percent in range(95):
            time.sleep(0.5)
            progress_bar.progress(percent + 1)
            loading_placeholder.text("🚀 Scanning the Universe..." if percent % 20 < 10 else "🌌 Fetching Cosmic Content...")

        try:
            # Direct API Call if Date is selected
            if st.session_state["last_updated"] == "selected_date":
                st.write(st.session_state["last_updated"])
                api_url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={query}"
                response = requests.get(api_url).json()
                data = {
                    "date": response["date"],
                    "title": response["title"],
                    "explanation": response["explanation"],
                    "media_type": response["media_type"],
                    "image_url": response.get("hdurl", response.get("url", "")),
                }
            else:
                response = requests.post("https://nasaapod.onrender.com/get_nasa_apod", json={"query": query})
                data = response.json()

            progress_bar.empty()
            loading_placeholder.empty()

            if "error" in data:
                st.error(data["error"])
            else:
                st.subheader(data["title"])
                st.write(f"**Date Derived:** {data['date']}")
                st.write(data["explanation"])

                if data["media_type"] == "image":
                    st.image(data["image_url"], caption="NASA Astronomy Picture of the Day", use_container_width=True)
                elif data["media_type"] == "video":
                    st.video(data["video_url"])

                # Reset State
                st.session_state["input_query"] = ""
                st.session_state["selected_date"] = None
                st.session_state["last_updated"] = None

        except Exception:
            st.error("Something went wrong. Please try again later.")
            st.write(Exception.args)
    else:
        st.warning("Please enter a query or select a date.")
