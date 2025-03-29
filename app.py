import pickle
import streamlit as st
import requests
import os

# Custom CSS for 3D-like design
st.markdown(
    """
    <style>
    /* Background styling */
    .stApp {
        background-image: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: white;
        font-family: 'Arial', sans-serif;
    }

    /* Header styling */
    header {
        text-align: center;
        color: #f9d423;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 20px;
        text-shadow: 3px 3px 6px #000000;
    }

    /* Dropdown and buttons styling */
    .stSelectbox, .stButton > button {
        background-color: #112b39;
        color: white;
        border: 2px solid #f9d423;
        border-radius: 10px;
        font-size: 16px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .stSelectbox:hover, .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px #f9d423;
        cursor: pointer;
    }

    /* Movie recommendations (3D cards) */
    .movie-card {
        background-color: #203a43;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .movie-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.8);
    }

    /* Text styling */
    .movie-title {
        color: #f9d423;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
                                                                         
f=open("key.txt")
key=f.read() 
       
# Function to fetch the poster of a movie using TMDB API
def fetch_poster(movie_id):
          
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=key"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except Exception as e:
        print(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=Error"

# Function to recommend movies based on the selected movie
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:  # Top 5 similar movies
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names, recommended_movie_posters
    except IndexError:
        return [], []

# Streamlit App
st.markdown("<header>🎥 Movie Recommendation System</header>", unsafe_allow_html=True)

# Load pre-trained data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# List of movie titles
movie_list = movies['title'].values

# Dropdown for selecting a movie
selected_movie = st.selectbox(
    "🌟 Type or select a movie from the dropdown:",
    movie_list
)

# Button to show recommendations
if st.button('✨ Show Recommendations'):
    if selected_movie:
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        if recommended_movie_names:
            # Display recommended movies in 3D-like cards
            cols = st.columns(5)  # Use 5 columns for 5 recommendations
            for i, col in enumerate(cols):
                with col:
                    st.markdown(
                        f"""
                        <div class="movie-card">
                            <img src="{recommended_movie_posters[i]}" alt="Poster" width="100%" style="border-radius: 10px;">
                            <div class="movie-title">{recommended_movie_names[i]}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        else:
            st.error("No recommendations found. Please try another movie.")
    else:
        st.warning("Please select a movie from the dropdown.")