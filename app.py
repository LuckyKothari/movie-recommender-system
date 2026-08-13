import pickle

import streamlit as st
from curl_cffi import requests
from curl_cffi.requests.exceptions import RequestException

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))


# --------------------------------------------------
# MOVIE RECOMMENDATION FUNCTION
# --------------------------------------------------

def recommend(movie_name):

    movie_index = movies[movies["title"] == movie_name].index[0]

    distances = sorted(
        list(enumerate(similarity[movie_index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movies = []

    for index, _ in distances[1:6]:

        recommended_movies.append(
            movies.iloc[index]["title"]
        )

    return recommended_movies


# --------------------------------------------------
# FETCH MOVIE POSTER FROM TMDB
# --------------------------------------------------

@st.cache_data(ttl=3600)
def fetch_poster(movie_name):

    token = st.secrets["TMDB_ACCESS_TOKEN"]

    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json"
    }

    url = "https://api.themoviedb.org/3/search/movie"

    for attempt in range(3):

        try:

            response = requests.get(
                url,
                headers=headers,
                params={"query": movie_name},
                impersonate="chrome",
                timeout=20
            )

            if response.status_code == 200:

                data = response.json()

                if data.get("results"):

                    poster_path = data["results"][0].get("poster_path")

                    if poster_path:

                        return (
                            "https://image.tmdb.org/t/p/w500"
                            + poster_path
                        )

                return None

        except RequestException:

            if attempt == 2:
                return None

    return None


# --------------------------------------------------
# FRONTEND
# --------------------------------------------------

st.title("🎬 Movie Recommender System")

st.write(
    "Discover movies similar to your favorite films using "
    "machine learning."
)


# --------------------------------------------------
# MOVIE SELECTION
# --------------------------------------------------

selected_movie = st.selectbox(
    "Select a movie",
    movies["title"].values
)


# --------------------------------------------------
# RECOMMEND BUTTON
# --------------------------------------------------

if st.button("🎯 Recommend"):

    recommendations = recommend(selected_movie)

    st.subheader("🍿 Recommended Movies")

    columns = st.columns(5)

    for index, movie in enumerate(recommendations):

        with columns[index]:

            poster = fetch_poster(movie)

            if poster:

                st.image(
                    poster,
                    use_container_width=True
                )

            else:

                st.info("Poster unavailable")

            st.caption(movie)