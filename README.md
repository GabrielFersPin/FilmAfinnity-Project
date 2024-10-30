# FilmAffinity Web Scraping Project

### Overview
This project was developed to explore web scraping techniques using **BeautifulSoup**. It focuses on extracting data from the **FilmAffinity** website to analyze Oscar-nominated actors and actresses, identifying their most iconic films by genre.

### Objective
The primary goal of this project is to:
- **Identify** the Oscar-nominated actors and actresses.
- **Categorize** their most famous films by genre.
- **Analyze** trends in film genres related to Oscar-nominated performances.

### Key Features
- **Data Extraction**: The project scrapes film data from FilmAffinity using BeautifulSoup, focusing on actors/actresses who have been nominated for Oscars.
- **Genre Classification**: Automatically classifies the films based on their genre.
- **Oscar-Nominated Performers**: Isolates actors and actresses who have been candidates for an Oscar, providing insights into their most significant works across different genres.
  
### Technologies Used
- **Python**: Core programming language for the project.
- **BeautifulSoup**: Web scraping library used to extract and parse data from HTML.
- **Pandas**: For data manipulation and analysis.
- **Requests**: To fetch HTML content from FilmAffinity.

### Screenshots
![Web scraping in action](images/Screenshot.png)
*Figure 1: Data extraction process.*

### Results

- **Comprehensive List**: A comprehensive list of Oscar-nominated actors and actresses, along with their most iconic films categorized by genre.
  
- **Nominations by Genre**: The analysis showed that the **action** genre received the highest number of nominations over the years, followed by **drama** and **comedy**.

  ![Nominations by Genre](images/nominations_by_genre.png)
  *Figure 2: Nominations by Genre over the Years*

- **Trend Analysis**: A linear regression analysis was performed to identify trends in nominations by genre. The results indicated an increasing trend in nominations for the **action** genre, while the **horror** genre showed a decline in nominations.

  ![Regression Analysis](images/regression_analysis.png)
  *Figure 3: Linear Regression of Nominations by Genre*

- **Top Performers**: The analysis identified the top-performing movies based on the number of nominations. For instance, **"Gladiator"** received the most nominations with **2 nominations**, highlighting its impact in the action genre.

  | Movie Title | Year | Genre   | Nominations |
  |-------------|------|---------|-------------|
  | Gladiator   | 2000 | Action  | 2           |


### Learnings
This project provided hands-on experience with:
- Web scraping using BeautifulSoup.
- Data processing and cleaning.
- Extracting meaningful insights from unstructured web data.
