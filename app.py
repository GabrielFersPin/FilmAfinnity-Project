import streamlit as st
import pandas as pd
# Import other necessary libraries

# Load your data
movies = pd.read_csv('src/results/movies.csv')
oscars = pd.read_csv('src/results/oscars.csv')
movies_oscars = pd.read_csv('src/results/movies_oscars.csv')

# Title
st.title("FilmAffinity Web Scraping Project")

# Overview
st.subheader("Overview")
st.write("This project was developed to explore web scraping techniques...")

# Display DataFrame
st.subheader("Movies and Oscars Data")
st.dataframe(movies_oscars)

# Analysis Section
st.subheader("Top Performers")
top_performers = movies_oscars.groupby('name')['nominations'].sum().reset_index()
top_performers = top_performers.sort_values(by='nominations', ascending=False)
st.write(top_performers)

# You can add more analysis or visualizations as needed
