import streamlit as st
import plotly.express as px
from backend import get_data
from datetime import datetime  

# Add title, text input, slider, selectbox and subheader
st.title("Weather Forecast for the Upcoming Days")
place = st.text_input("Place: ") # Interracive widgets normally should have variables
days = st.slider("Forecast Days", min_value=1, max_value=5, help="Select the number of days to be displayed")
option = st.selectbox("Select data to view", ("Temperature", "Sky"))
if option == "Temperature":
    degree_option = st.selectbox("Select degree type", ("Celsius", "Farenheit"))

st.subheader(f"{option} for the next {days} days in {place}")


if place: # In that case, it doesn't show anything if place is not provided (thus avoid getting an error. It only shows valid info if place is provided)    
    # Get temperature/sky data
    try:
        filtered_data = get_data(place, days)
        if option == "Temperature":
            if degree_option == "Celsius":  
                temperatures = [(dict["main"]["temp"]) for dict in filtered_data]
                dates = [dict["dt_txt"] for dict in filtered_data]
            else:
                temperatures = [(dict["main"]["temp"])* (9/5) + 32 for dict in filtered_data]
                dates = [dict["dt_txt"] for dict in filtered_data]
            # Create temperature plot
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y":f'Temperature ({degree_option})'})
            st.plotly_chart(figure)
        if option == "Sky":
            # building dictionary to associate keywords with pictures for the weather conditions
            images = {"Clear":"images/clear.png", "Clouds":"images/cloud.png", "Rain":"images/rain.png", "Snow":"images/snow.png"}
            
            # Creating timestamps for condition option.
            condition_date = [dict["dt_txt"] for dict in filtered_data]
            # strptime refers to parsing time which is used to read time in specific format.
            condition_date = [datetime.strptime(i,"%Y-%m-%d %H:%M:%S") for i in condition_date]
            # Whereas strftime refers to formatting time, which we use to change the format of time to some new format. 
            final = [i.strftime("%a, %b %d, %Y %H:%M") for i in condition_date]
            # Filtering sky conditions from the API data
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            # Building list comprehension to associate the condition with the image
            image_render = [images[condition] for condition in sky_conditions]
            st.image(image_render, width = 115, caption=final)
    except KeyError:
        st.write("That place does not exist!")