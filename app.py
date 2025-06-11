import pickle
import streamlit as st
import requests


# Function to fetch movie posters from TMDB API
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path', None)
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image+Available"  # Placeholder for missing posters
    except Exception as e:
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Poster"


# Function to recommend movies
def recommend(movie_name):
    try:
        index = movie[movie['title'] == movie_name].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:  # Top 5 recommendations
            movie_id = movie.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movie.iloc[i[0]].title)

        return recommended_movie_names, recommended_movie_posters
    except IndexError:
        return ["No recommendations found"], ["https://via.placeholder.com/500x750?text=No+Image+Available"]


# Streamlit app
st.header('Movie Recommender System')

# Load movie data and similarity matrix
movie = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Dropdown for movie selection
movie_list = movie['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Display recommendations
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Create columns for displaying recommendations
    cols = st.columns(5)
    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.text(name)
            st.image(poster)
