import streamlit as st
import pickle
import requests

movies_list = pickle.load(open('movies.pkl','rb'))
similar_movies_table = pickle.load(open('similar_movies.pkl','rb'))

movies_list2 = movies_list['title'].values
st.title("Movies Recommender System")

def fetch_poster(movie_id):
   response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c444cad898385b4459caf017cb4d9797&language=en-US'.format(movie_id))
   data = response.json()
   return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
  movie_index = movies_list[movies_list['title']==movie].index[0]
  distances = similar_movies_table[movie_index]
  similar_movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x:x[1])[1:6]
  recommended_movies_poster = []
  recommended_movies_names = []
  for i in similar_movies_list:
    movie_id = movies_list.iloc[i[0]].movie_id
    recommended_movies_names.append(movies_list.iloc[i[0]].title)
    recommended_movies_poster.append(fetch_poster(movie_id))
  return recommended_movies_names,recommended_movies_poster


selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies_list2)

if st.button('Recommend'):
    names,poster = recommend(selected_movie_name)

    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
       st.text (names[0])
       st.image(poster[0])
    with col2:
       st.text (names[1])
       st.image(poster[1])
    with col3:
       st.text (names[2])
       st.image(poster[2])
    with col4:
       st.text (names[3])
       st.image(poster[3])
    with col5:
       st.text (names[4])
       st.image(poster[4])
else :
    st.write('No movies Selected till now ')

# https://api.themoviedb.org/3/movie/movie_id?language=en-US