from flask import Flask, render_template, request
import requests
import os

def process_image_urls(data, width='w500'):
    if isinstance(data, list):
        for item in data:
            process_image_urls(item, width)
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                process_image_urls(value, width)
            elif 'namePoster' in key and '{width_variable}' in value:
                data[key] = value.replace('{width_variable}', width) if value else DEFAULT_PERSON_IMAGE_URL
            elif 'titlePoster' in key and '{width_variable}' in value:
                data[key] = value.replace('{width_variable}', width) if value else DEFAULT_MOVIE_IMAGE_URL

app = Flask(__name__)
app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

API_BASE_URL = 'http://localhost:9876/ntuaflix_api'

# Dummy data for fallback
DUMMY_GENRES_DATA = {
    'Action': [{'title': 'Dummy Movie 1', 'rating': {'avRating': '7.8'}, 'titlePoster': 'path/to/poster1.jpg'}],
    'Drama': [{'title': 'Dummy Movie 2', 'rating': {'avRating': '8.2'}, 'titlePoster': 'path/to/poster2.jpg'}]
}
DUMMY_MOVIES = [{'title': 'Dummy Movie', 'rating': {'avRating': '7.5'}, 'titlePoster': 'path/to/poster.jpg'}]
DUMMY_ACTOR = {'name': 'Dummy Actor', 'bio': 'This is a dummy bio', 'img_url_asset': 'path/to/actor.jpg'}
DUMMY_MOVIE_DETAILS = {'title': 'Dummy Movie', 'rating': {'avRating': '8.1'}, 'genres': ['Action', 'Drama']}
DUMMY_SERIES_DETAILS = {'title': 'Dummy Series', 'summary': 'This is a dummy series'}

@app.route('/')
def homepage():
    try:
        response = requests.get(f"{API_BASE_URL}/top10bygenre")
        genres_data = response.json() if response.status_code == 200 else {}
        process_image_urls(genres_data)
    except requests.RequestException:
        genres_data = DUMMY_GENRES_DATA
    return render_template('homepage.html', genres_data=genres_data)

@app.route('/search')
def searchpage():
    query = request.args.get('query', '')
    # Initialize empty lists for movies and actors
    movies = []
    actors = []

    # Search for movies
    try:
        response = requests.get(f"{API_BASE_URL}/searchtitle", json={'titlePart': query})
        movies = response.json() if response.status_code == 200 else []
    except requests.RequestException:
        movies = []

    # Search for actors
    try:
        response = requests.get(f"{API_BASE_URL}/searchname", json={'namePart': query})
        actors = response.json() if response.status_code == 200 else []
        for actor in actors:
            for title in actor["nameTitles"]:
                titleID = title["titleID"]
                title_response = requests.get(f"{API_BASE_URL}/title/{titleID}")
                if title_response.status_code == 200:
                    title_details = title_response.json()
                    process_image_urls(title_details, 'w500')
                    movies.append(title_details)
        process_image_urls(actors)
        process_image_urls(movies)
    except requests.RequestException:
        # If there's no specific dummy data for actors, you could define some or use an empty list as a fallback
        actors = []

    # Pass both movies and actors to the template
    return render_template('searchpage.html', movies=movies, actors=actors)

@app.route('/actor/<actor_name>')
def actor_page(actor_name):
    try:
        response = requests.get(f"{API_BASE_URL}/name/{actor_name}")
        actor_details = response.json() if response.status_code == 200 else {}
        process_image_urls(actor_details)
        movies = []
        for title in actor_details["nameTitles"]:
            titleID = title["titleID"]
            title_response = requests.get(f"{API_BASE_URL}/title/{titleID}")
            if title_response.status_code == 200:
                title_details = title_response.json()
                process_image_urls(title_details, 'w500')
                movies.append(title_details)
        actor_details["movies"] = movies
    except requests.RequestException:
        actor_details = DUMMY_ACTOR
    return render_template('actor_page.html', actor=actor_details)


@app.route('/movie/<movie_title>')
def movie_page(movie_title):
    try:
        response = requests.get(f"{API_BASE_URL}/title/{movie_title}")
        movie_details = response.json() if response.status_code == 200 else {}

        cast = []
        crew = {"directors": [], "writers": []}
        for principal in movie_details.get("principals", []):
            nameID = principal.get("nameID", "")
            category = principal.get("category", "")
            name_response = requests.get(f"{API_BASE_URL}/name/{nameID}")
            if name_response.status_code == 200:
                name_info = name_response.json()

                if category in ["actor", "actress"]:
                    cast.append(name_info)
                elif category == "director":
                    crew["directors"].append(name_info)
                elif category == "writer":
                    crew["writers"].append(name_info)

        movie_details["cast"] = cast
        movie_details["crew"] = crew
        process_image_urls(movie_details)
    except requests.RequestException:
        movie_details = DUMMY_MOVIE_DETAILS

    return render_template('movie_page.html', movie=movie_details)



@app.route('/series/<series_title>')
def series_page(series_title):
    try:
        response = requests.get(f"{API_BASE_URL}/title/{series_title}")
        series_details = response.json() if response.status_code == 200 else {}
    except requests.RequestException:
        series_details = DUMMY_SERIES_DETAILS
    return render_template('series_page.html', series=series_details)

@app.route('/genre/<genre_name>')
def genre_page(genre_name):
    try:
        response = requests.get(f"{API_BASE_URL}/bygenre", json={'qgenre': genre_name, 'minrating': '0'})
        movies = response.json() if response.status_code == 200 else []
        process_image_urls(movies)
    except requests.RequestException:
        # Fallback to dummy data for the genre
        movies = DUMMY_GENRES_DATA.get(genre_name, [])
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

