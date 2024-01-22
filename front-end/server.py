from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)
app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

API_BASE_URL = 'http://localhost:9876/ntuaflix_api'

@app.route('/')
def homepage():
    response = requests.get(f"{API_BASE_URL}/top10bygenre")
    if response.status_code == 200:
        genres_data = response.json()
    else:
        genres_data = {}
    return render_template('homepage.html', genres_data=genres_data)

@app.route('/search')
def searchpage():
    query = request.args.get('query', '')
    response = requests.get(f"{API_BASE_URL}/searchtitle", json={'titlePart': query})
    movies = response.json() if response.status_code == 200 else []
    return render_template('searchpage.html', movies=movies)

@app.route('/actor/<actor_name>')
def actor_page(actor_name):
    response = requests.get(f"{API_BASE_URL}/name/{actor_name}")
    actor_details = response.json() if response.status_code == 200 else {}
    return render_template('actor_page.html', actor=actor_details)

@app.route('/movie/<movie_title>')
def movie_page(movie_title):
    response = requests.get(f"{API_BASE_URL}/title/{movie_title}")
    movie_details = response.json() if response.status_code == 200 else {}
    return render_template('movie_page.html', movie=movie_details)

@app.route('/series/<series_title>')
def series_page(series_title):
    response = requests.get(f"{API_BASE_URL}/title/{series_title}")
    series_details = response.json() if response.status_code == 200 else {}
    return render_template('series_page.html', series=series_details)

@app.route('/genre/<genre_name>')
def genre_page(genre_name):
    response = requests.get(f"{API_BASE_URL}/bygenre", json={'qgenre': genre_name, 'minrating': '0'})
    movies = response.json() if response.status_code == 200 else []
    return render_template('genre_page.html', genre_name=genre_name, movies=movies)

if __name__ == "__main__":
    app.run(debug=True)



# from flask import Flask, render_template
# import os

# app = Flask(__name__)

# # Set the templates folder to the "templates" subdirectory
# app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')


# # Define sample data (replace this with your actual data)
# genres = ['Action', 'Drama', 'Comedy']
# movies = [
#     {'title': 'Movie 1', 'rating': 8.5, 'genre': 'Action'},
#     {'title': 'Movie 2', 'rating': 7.9, 'genre': 'Drama'},
#     {'title': 'Movie 3', 'rating': 6.5, 'genre': 'Comedy'},
# ]
# actors = [
#     {'name': 'Actor 1', 'bio': 'Bio for Actor 1'},
#     {'name': 'Actor 2', 'bio': 'Bio for Actor 2'},
# ]

# # Define routes
# @app.route('/')
# def homepage():
#     return render_template('homepage.html', genres=genres, movies=movies)

# @app.route('/search')
# def searchpage():
#     return render_template('searchpage.html', movies=movies, actors=actors)

# @app.route('/actor/<actor_name>')
# def actor_page(actor_name):
#     # Fetch actor details from the database based on actor_name
#     actor_details = {'name': actor_name, 'bio': 'Bio for ' + actor_name}
#     return render_template('actor_page.html', actor=actor_details)

# @app.route('/movie/<movie_title>')
# def movie_page(movie_title):
#     # Fetch movie details from the database based on movie_title
#     movie_details = {'title': movie_title, 'rating': 8.5, 'genre': 'Action'}
#     return render_template('movie_page.html', movie=movie_details)

# @app.route('/series/<series_title>')
# def series_page(series_title):
#     # Fetch series details from the database based on series_title
#     series_details = {'title': series_title, 'seasons': 5, 'episodes': 10}
#     return render_template('series_page.html', series=series_details)

# @app.route('/genre/<genre_name>')
# def genre_page(genre_name):
#     # Fetch movies in the specified genre from the database
#     genre_movies = [movie for movie in movies if movie['genre'] == genre_name]
#     return render_template('genre_page.html', genre_name=genre_name, movies=genre_movies)


# app.run(debug=True)

