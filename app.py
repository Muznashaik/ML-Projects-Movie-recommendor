from datetime import datetime
import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie, date_of_birth):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


def signup():
    st.subheader("Signup")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    return username, email, password


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender')

if "page" not in st.session_state:
    st.session_state.page = "Signup"

if st.session_state.page == "Signup":
    username, email, password = signup()
    if st.button("Submit"):
        # Process signup data here
        st.write("Signup Successful!")

        # Redirect to the home page after successful signup
        st.session_state.page = "Home"

elif st.session_state.page == "Home":
    st.sidebar.markdown("### Movie Recommender")
    selected_movie_name = st.selectbox("Select a movie", movies['title'].values)
    max_date = datetime.now().date()
    min_date = datetime(1990, 1, 1).date()
    date_of_birth = st.date_input("Select Date of Birth", min_value=min_date, max_value=max_date)

    if st.button('Recommend Movie'):
        names, posters = recommend(selected_movie_name, date_of_birth)
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])
