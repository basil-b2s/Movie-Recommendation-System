import pickle 
import streamlit as st
import requests


st.set_page_config(
    page_title="Movie Recommnedation System",
    page_icon="🧊",
    layout="wide",

)

st.markdown(
    """
    <style>
    body {
        background-color: #g0f0f0; /* Use your preferred shade of grey */
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("Movie Recommnedation System")


movies = pickle.load(open('models/movies.pkl','rb'))
sim_vectors = pickle.load(open('models/similarity.pkl','rb'))

def movie_poster(id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=YourAPIKey&language=en-US".format(id) # please choose your api key here
    data = requests.get(url)
    data = data.json()
    poster = data['poster_path']
    path = "https://image.tmdb.org/t/p/w500/" + poster
    return path
def recommend(movie):
    rec_movies = []
    rec_movie_posters = []
    movie_index = movies[movies['title'] == movie].index[0]
    vector = sim_vectors[movie_index]
    movie_list = sorted(enumerate(vector), reverse=True, key=lambda x:x[1])[1:7]
    for i in movie_list[1:7]:
        movie_id = movies.iloc[i[0]].movie_id
        rec_movies.append(movies.iloc[i[0]].title)
        rec_movie_posters.append(movie_poster(movie_id))
    return rec_movies, rec_movie_posters

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie",movie_list
)

if st.button('Recommend'):
    rec_movies, rec_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(rec_movies[0])
        st.image(rec_movie_posters[0])
    with col2:
        st.text(rec_movies[1])
        st.image(rec_movie_posters[1])

    with col3:
        st.text(rec_movies[2])
        st.image(rec_movie_posters[2])
    with col4:
        st.text(rec_movies[3])
        st.image(rec_movie_posters[3])
    with col5:
        st.text(rec_movies[4])
        st.image(rec_movie_posters[4])