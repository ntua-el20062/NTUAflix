from flask import Flask, render_template, request
import requests
import os

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

DEFAULT_MOVIE_IMAGE_URL = "https://icons.iconarchive.com/icons/designbolts/free-multimedia/512/Film-icon.png"
DEFAULT_PERSON_IMAGE_URL = "https://cdn-icons-png.flaticon.com/512/3060/3060028.png"

def process_image_urls(data, width='w500'):
    if isinstance(data, list):
        for item in data:
            process_image_urls(item, width)
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                process_image_urls(value, width)
            elif 'namePoster' in key:
                if value and '{width_variable}' in value:
                    data[key] = value.replace('{width_variable}', width)
                else:
                    data[key] = DEFAULT_PERSON_IMAGE_URL
            elif 'titlePoster' in key:
                if value and '{width_variable}' in value:
                    data[key] = value.replace('{width_variable}', width)
                else:
                    data[key] = DEFAULT_MOVIE_IMAGE_URL


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
    try:
        # Fetch movies
        response_movies = requests.get(f"{API_BASE_URL}/searchtitle", json={'titlePart': query})
        movies = response_movies.json() if response_movies.status_code == 200 else []
        process_image_urls(movies)

        # Fetch people
        response_people = requests.get(f"{API_BASE_URL}/searchname", json={'namePart': query})
        people = response_people.json() if response_people.status_code == 200 else []
        print(people)
        process_image_urls(people)

    except requests.RequestException:
        movies = DUMMY_MOVIES
        people = []  # Add dummy data for people if needed

    return render_template('searchpage.html', movies=movies, actors=people)


#something needs to change here in order to get the movie title 
@app.route('/actor/<actor_name>')
def actor_page(actor_name):
    try:
        response = requests.get(f"{API_BASE_URL}/name/{actor_name}")
        actor_details = response.json() if response.status_code == 200 else {}
    except requests.RequestException:
        actor_details = DUMMY_ACTOR
    return render_template('actor_page.html', actor=actor_details)

@app.route('/movie/<movie_title>')
def movie_page(movie_title):
    try:
        response = requests.get(f"{API_BASE_URL}/title/{movie_title}")
        movie_details = response.json() if response.status_code == 200 else {}
        names = []
        for principal in movie_details["principals"]:
            nameID = principal["nameID"]
            name_response = requests.get(f"{API_BASE_URL}/name/{nameID}")
            if name_response.status_code == 200:
                names.append(name_response.json())
        movie_details["names"] = names

    except requests.RequestException:
        movie_details = DUMMY_MOVIE_DETAILS
    return render_template('movie_page.html', movie=movie_details)

@app.route('/series/<series_title>')
def series_page(series_title):
    try:
        response = requests.get(f"{API_BASE_URL}/title/{series_title}")
        series_details = response.json() if response.status_code == 200 else {}
        process_image_urls(series_details)
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
        movies = DUMMY_GENRES_DATA.get(genre_name, [])
    return render_template('genre_page.html', genre_name=genre_name, movies=movies)

if __name__ == "__main__":
    app.run(debug=True)

