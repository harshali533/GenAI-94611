import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

st.set_page_config(page_title="Login Weather App")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "logout" not in st.session_state:
    st.session_state.logout = False

#LOGIN PAGE 
if not st.session_state.logged_in and not st.session_state.logout:
    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == password and username != "":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.write("Invalid credentials")

#WEATHER PAGE
elif st.session_state.logged_in:
    st.title("Weather Information")

    city = st.text_input("Enter city name")

    if st.button("Get Weather") and city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        st.subheader(f"Weather in {city}")
        st.write("Temperature:", data["main"]["temp"], "°C")
        st.write("Humidity:", data["main"]["humidity"], "%")
        st.write("Condition:", data["weather"][0]["description"])

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.logout = True
        st.rerun()

#LOGOUT PAGE
elif st.session_state.logout:
    st.title("Thank You!")
    st.write("You have successfully logged out.")
