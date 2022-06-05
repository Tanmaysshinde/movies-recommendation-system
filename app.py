import streamlit as st
import pickle as pk
import difflib
import requests
import dropbox
from dropbox.exceptions import AuthError
import os

DROPBOX_ACCESS_TOKEN = 'sl.BI8TAN6AFUxi9YppRePBrnqDGxugh_LKH4wR0G3ljq7ONPGC8Hz-Gg74MPXLNC2WoAC26c6v6aEQjFvmrngOtt411puF7kD4ZiwrmadPYCsujCd_mX9XbpunZ28Wjaq3mNJjLPPgw-U'

def dropbox_connect():
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        print('...authenticated with Dropbox owned by ' + dbx.users_get_current_account().name.display_name)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx

def dropbox_download_file():
    global similarity
    try:
        dbx = dropbox_connect()

        with open('similarity.pkl', 'wb') as f:
            metadata, result = dbx.files_download(path='id:ERdBKSH3-FAAAAAAAAAADQ')
            f.write(result.content)
            print('success')
            similarity = pk.load(open('similarity.pkl', 'rb'))
    except Exception as e:
        print('Error downloading file from Dropbox: ' + str(e))

def recommend(movie):
    list_of_title = movies_list['title'].tolist()
    all_close_match = difflib.get_close_matches(movie, list_of_title)
    close_match = all_close_match[0]
    movie_index = movies_list[movies_list['title'] == close_match].index[0]
    similarity_score = list(enumerate(similarity[movie_index]))
    similar_movies = sorted(similarity_score, key = lambda x : x[1], reverse = True)[1:11]
    recommend_movies = []
    recommend_movies_posters = []
    for i in similar_movies:
        movie_id = movies_list.iloc[i[0]].id
        recommend_movies.append(movies_list.iloc[i[0]].title)
        recommend_movies_posters.append(movie_poster(movie_id))
    return recommend_movies, recommend_movies_posters

def movie_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=4398e9f2521e6b1ba0a76e8c5a547a7c&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

movies_list = pk.load(open('movies.pkl', 'rb'))
movies_title_list = movies_list['title'].values

if os.path.isfile('./similarity.pkl') == False:
    dropbox_download_file()
else:
    similarity = pk.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendation System')

user_movie_name = st.selectbox(
    'Movie Name',
    movies_title_list
)

if st.button('Recommend Movies'):
    names, posters = recommend(user_movie_name)
    movie1, movie2, movie3 = st.columns(3)
    with movie1:
        st.header(names[0])
        st.image(posters[0])
    with movie2:
        st.header(names[1])
        st.image(posters[1])
    with movie3:
        st.header(names[2])
        st.image(posters[2])

    movie4, movie5, movie6 = st.columns(3)
    with movie4:
        st.header(names[3])
        st.image(posters[3])
    with movie5:
        st.header(names[4])
        st.image(posters[4])
    with movie6:
        st.header(names[5])
        st.image(posters[5])

    movie7, movie8, movie9 = st.columns(3)
    with movie7:
        st.header(names[6])
        st.image(posters[6])
    with movie8:
        st.header(names[7])
        st.image(posters[7])
    with movie9:
        st.header(names[8])
        st.image(posters[8])

    movie10, movie11, movie12 = st.columns(3)
    with movie10:
        st.header(names[9])
        st.image(posters[9])
    with movie11:
        st.header('')
    with movie12:
        st.header('')
