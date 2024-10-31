import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
# Import other necessary libraries

# Load your data
movies = pd.read_csv('src/results/movies.csv')
oscars = pd.read_csv('src/results/oscars.csv')
movies_oscars = pd.read_csv('src/results/movies_oscars.csv')

# Title
st.set_page_config(page_title="FilmAffinity Web Scraping Project", page_icon="🎬")
st.title("🎬 FilmAffinity Web Scraping Project")

# Overview
st.subheader("Overview")
st.write("This project was developed to extract data from [FilmAffinty website](https://www.filmaffinity.com/us/topgen.php?genres=%2BHO&chv=0&orderby=rc&movietype=movie%7C&country=&fromyear=1980&toyear=2023&ratingcount=2&runtimemin=0&runtimemax=4) and make a further analysis.")

movies = movies.reset_index(drop=True)
# Show a multiselect widget with the genres using `st.multiselect`.
genres = st.multiselect(
    "Genres",
    options=movies['genre'].unique().tolist(),
    default=["action", "comedy", "drama", "horror"]
)

# Show a slider widget with the years using `st.slider`.
years = st.slider("Years", 1980, 2024, (2000, 2024))

# Filter the dataframe based on the widget input and reshape it.
df_filtered = movies[(movies["genre"].isin(genres)) & (movies["year"].between(years[0], years[1]))]

# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_filtered,
    use_container_width=True,
    column_config={"year": st.column_config.TextColumn("Year")},
)


# Display Movies and Oscars Data
st.subheader("Movies and Oscars Data")
columns_to_drop = ['Unnamed: 0', 'Unnamed: 0_x', 'Unnamed: 0_y']  # Specify the columns you want to drop
movies_oscars = movies_oscars.drop(columns=columns_to_drop)
st.dataframe(movies_oscars)

# Analysis Section
st.subheader("Top Performers")
top_performers = movies_oscars.groupby('name')['nominations'].sum().reset_index()
top_performers = top_performers.sort_values(by='nominations', ascending=False)
st.write(top_performers)

#Movies with the most nominations
st.subheader('Movies with most nominations')
movie_nominations = movies_oscars.groupby('title')['nominations'].sum().reset_index()
movie_nominations = movie_nominations.sort_values(by='nominations', ascending=False)
top_movie = movie_nominations.head(3)
st.write(top_movie)

#Display the graph of how the nominations changed over the years
st.subheader("How nominations changed over the years")
nominations_by_genre = movies_oscars.groupby(['year', 'genre'])['nominations'].sum().reset_index()
fig = px.bar(nominations_by_genre, x="year", y="title", color="genre", title="Nominations by Genre")
st.plotly_chart(fig)


