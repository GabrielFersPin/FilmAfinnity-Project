import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import statsmodels.api as sm
import plotly.graph_objs as go
# Import other necessary libraries

# Load your data
movies = pd.read_csv('src/results/movies.csv')
oscars = pd.read_csv('src/results/oscars.csv')
movies_oscars = pd.read_csv('src/results/movies_oscars.csv')
top_performers = pd.read_csv('src/results/top_performers.csv')

columns_to_drop = ['Unnamed: 0', 'Unnamed: 0_x', 'Unnamed: 0_y']  # Specify the columns you want to drop
movies_oscars = movies_oscars.drop(columns=columns_to_drop, errors='ignore')

# Title
st.set_page_config(page_title="Movie Selection", page_icon="🎬")
st.title("🎬 Find Your Movie")

# Overview
st.subheader("Overview")
st.write("This app was developed to make a movie selection based on the 30 best movies of each genre from [FilmAffinty website](https://www.filmaffinity.com/us/topgen.php?genres=%2BHO&chv=0&orderby=rc&movietype=movie%7C&country=&fromyear=1980&toyear=2023&ratingcount=2&runtimemin=0&runtimemax=4) and make a further analysis.")

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

movies_oscars = pd.DataFrame(movies_oscars)

# Remove commas from the 'year' column
movies_oscars['year'] = movies_oscars['year'].astype(str).str.replace(',', '', regex=False)

# Title and search bar
st.title("Movie Search")
search_query = st.text_input("Search for a movie title", "")

# Confirm the search query input
st.write("Search Query:", search_query)  # This line helps check if the query is captured

# Filter the DataFrame based on the search query
if search_query.strip():  # Checks if there's any non-whitespace input
    movie_filtered = movies_oscars[movies_oscars["title"].str.contains(search_query, case=False, na=False)]
else:
    movie_filtered = movies_oscars
    
# Display Filtered Movies and Oscars Data
st.subheader("Movies and Oscars Data")
st.dataframe(movie_filtered)

# Top performers search bar
st.title("Top performers Search")
search_query = st.text_input("Search for a actor/actress", "")

# Confirm the search query input
st.write("Search Query:", search_query)  # This line helps check if the query is captured

# Filter the DataFrame based on the search query
if search_query.strip():  # Checks if there's any non-whitespace input
    filter_performers = top_performers[top_performers["name"].str.contains(search_query, case=False, na=False)]
else:
    filter_performers = top_performers

filter_performers.drop(columns='Unnamed: 0', inplace=True)
        
# Analysis Section
st.subheader("Top Performer")
st.write(filter_performers)

#Movies with the most nominations
st.subheader('Movies with most nominations')
movie_nominations = movies_oscars.groupby('title')['nominations'].sum().reset_index()
movie_nominations = movie_nominations.sort_values(by='nominations', ascending=False)
top_movie = movie_nominations.head(5)
st.write(top_movie)

#Genres with most nominations
st.subheader('Genres with most nominations')
most_nominations = movies_oscars.groupby("genre")["nominations"].sum().sort_values(ascending=False)
st.write(most_nominations)

#Display the graph of how the nominations changed over the years
st.subheader("How nominations changed over the years")
nominations_by_genre = movies_oscars.groupby(['year', 'genre'])['nominations'].sum().reset_index()

fig = px.line(
    nominations_by_genre,  
    x="year",     
    y="nominations",  
    color="genre",    
    title="Nominations by Genre"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Number of Nominations",
    legend_title="Genre",
)

st.plotly_chart(fig)

