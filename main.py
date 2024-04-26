import streamlit as st
import plotly.express as px

st.title("Weather Forecast for the Upcoming Days")
place = st.text_input("Place: ") # Interracive widgets normally should have variables
days = st.slider("Forecast Days", min_value=1, max_value=5, help="Select the number of days to be displayed")
option = st.selectbox("Select data to view", ("Temperature", "Sky"))
if option == "Temperature":
    degree_option = st.selectbox("Select degree type", ("Celsius", "Farenheit"))

st.subheader(f"{option} for the next {days} days in {place}")

# Adding the graph
def get_data(days):    
    dates = ["2024", "2025", "2026"]
    temperatures = [3, 5, 7]
    temperatures = [days*i for i in temperatures]
    return dates, temperatures

d,t = get_data(days)

figure = px.line(x=d, y=t, labels={"x": "Date", "y":f'Temperature ({degree_option})'})
st.plotly_chart(figure)