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

st.subheader('Prediction to know how the nominations by genre will be for the next 5 years')
# Define the future years you want to predict
future_years = pd.DataFrame({'year': range(2024, 2029)})  # Predicting for the next 5 years

# Create a Plotly figure
fig = go.Figure()

for genre in nominations_by_genre['genre'].unique():
    genre_data = nominations_by_genre[nominations_by_genre['genre'] == genre]

    # Fit the linear regression model
    X = genre_data['year']
    y = genre_data['nominations']
    X = sm.add_constant(X)  # Add a constant term for the intercept

    model = sm.OLS(y, X).fit()

    # Plot original nominations data
    fig.add_trace(go.Scatter(
        x=genre_data['year'],
        y=genre_data['nominations'],
        mode='markers',
        name=f'{genre} (historical)',
        marker=dict(size=10)
    ))

    # Plot the regression line
    fig.add_trace(go.Scatter(
        x=genre_data['year'],
        y=model.predict(X),
        mode='lines',
        name=f'{genre} (fit)',
        line=dict(dash='dash')
    ))

    # Predict for future years
    future_X = sm.add_constant(future_years)
    future_predictions = model.predict(future_X)

    # Plot future predictions
    fig.add_trace(go.Scatter(
        x=future_years['year'],
        y=future_predictions,
        mode='lines+markers',
        name=f'{genre} (predictions)',
        line=dict(dash='dot')
    ))

# Customize the layout
fig.update_layout(
    title='Predicted Trends of Nominations by Genre',
    xaxis_title='Year',
    yaxis_title='Number of Nominations',
    xaxis=dict(tickvals=list(range(1980, 2030, 2))),
    legend=dict(x=0, y=1),
    template='plotly_white'
)

# Display the plot in Streamlit
st.plotly_chart(fig)

