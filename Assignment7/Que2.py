import streamlit as st
import requests
import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page title
st.set_page_config(page_title="Weather Explanation App", layout="centered")
st.title("🌤️ Weather Explanation App")

# City input
city = st.text_input("Enter city name (e.g., Pune, Mumbai):")

# Initialize LLM (Groq)
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# Button
if st.button("Get Weather"):
    if city.strip() == "":
        st.warning("Please enter a city name.")
    else:
        # Fetch weather data
        weather_api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"

        response = requests.get(url)
        data = response.json()

        # Check API response
        if data.get("cod") != 200:
            st.error("City not found or Weather API error.")
        else:
            # Extract weather details
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["description"]

            # Display raw weather data
            st.subheader("Current Weather")
            st.write(f" Temperature: {temp} °C")
            st.write(f" Feels Like: {feels_like} °C")
            st.write(f" Humidity: {humidity}%")
            st.write(f" Condition: {condition}")

            # LLM prompt
            prompt = f"""
            City: {city}
            Temperature: {temp} °C
            Feels Like: {feels_like} °C
            Humidity: {humidity}%
            Weather Condition: {condition}

            Explain the current weather in very simple English for a common person.
            """

            # Generate explanation
            with st.spinner("Explaining weather in simple English..."):
                explanation = llm.invoke(prompt)

            st.subheader("Weather Explanation")
            st.write(explanation.content)
