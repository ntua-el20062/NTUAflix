from flask import Flask, request, jsonify, make_response, session
from flask_mysqldb import MySQL
import pymysql
from flask_restful import Api, Resource, reqparse
from functools import wraps
import json, jwt, datetime
import mysql.connector

app = Flask(__name__)

#app.config["SECRET_KEY"] = "SECRET_KEY"
app.config["MYSQL_DB"] = "ntuaflix"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_HOST"] = "127.0.0.1"


def execute_query(query: str, values=None, fetch_data_flag=False, fetch_all_flag=False):
    """
    Executes a given query. Either for retrieval or update purposes.
    Args:
        query: Query to be executed
        values: Query values
        fetch_data_flag: Flag that signals a retrieval query
        fetch_all_flag: Flag that signals retrieval of all table data or just the first row.
    Returns:
        The data fetched for a specified query. If it is not a retrieval query then None is returned. 
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='ntuaflix'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, values) if values is not None else cursor.execute(query)
        fetched_data = (cursor.fetchall() if fetch_all_flag else cursor.fetchone()[0]) if fetch_data_flag else None
        cursor.close()
        connection.commit()
        connection.close()        
        return fetched_data
    except Exception as e:
        print(f'Query execution failed with error:\n{e}')


########################## Διαχειριστικές Απαιτήσεις ##################################
#######################################################################################

class health_check(Resource):
    def get(self):
            return {"status": "OK", "dataconnection":"change this to your connection"}, 200

#κάτι τέτοιο πρέπει να κάνετε για όλα τα insertions
class title_basics(Resource):
    def post(self):
        tsv_data = request.form.get("tsv_data")

        #{Επεξεργασία του tsv_data
        #.
        #.
        #.
        #.
        #.
        #Επεξεργασία του tsv_data}

        #Query για την εισαγωγή (INSERT)
        query = "SHOW TABLES"

        cur = db.get_db().cursor()
        cur.execute(query)
        db.get_db().commit()
        cur.close()

        return {"status":"Titles added"}, 200

class title_akas(Resource):
    def post(self):
        return {"status":"Akas added"}, 200

class name_basics(Resource):
    def post(self):
        return {"status":"Names added"}, 200

class title_crew(Resource):
    def post(self):
        return {"status":"Crew added"}, 200

class title_episode(Resource):
    def post(self):
        return {"status":"Episodes added"}, 200

class title_principal(Resource):
    def post(self):
        return {"status":"Principals added"}, 200

class title_ratings(Resource):
    def post(self):
        return {"status":"Ratings added"}, 200

class reset_all(Resource):
    def post(self):
        return {"message": "Reset All"}


########################### Λειτουργικές Απαιτήσεις ##################################
#######################################################################################

def create_title_object(titleID):
    title_query = "SELECT * FROM titlebasics WHERE tconst = %s"
    title_rows = execute_query(title_query, (titleID, ), fetch_data_flag=True, fetch_all_flag=True)
    
    if not title_rows:
        return None

    title_row = title_rows[0]
    titleObject = {
        "titleID": title_row["tconst"],
        "type": title_row["titleType"],
        "originalTitle": title_row["originalTitle"],
        "titlePoster": title_row["img_url_asset"],
        "startYear": str(title_row["startYear"]),
        "endYear": str(title_row["endYear"]) if title_row["endYear"] else None,
        "genres": title_row["genres"].split(",") if title_row["genres"] else []
    }

    aka_query = "SELECT title, region FROM akas WHERE titleId = %s"
    title_akas = execute_query(aka_query, (titleID,), fetch_data_flag=True, fetch_all_flag=True)
    titleObject["titleAkas"] = [{"akaTitle": row["title"], "regionAbbrev": row["region"]} for row in title_akas]
    
    principals_query = """
    SELECT pt.nconst, pt.category, p.primaryName 
    FROM principals pt
    JOIN namebasics p ON pt.nconst = p.nconst
    WHERE pt.tconst = %s
    """
    principals_data = execute_query(principals_query, (titleID,), fetch_data_flag=True, fetch_all_flag=True)
    principals = [
        {
            "nameID": row["nconst"],
            "name": row["primaryName"],
            "category": row["category"]
        } for row in principals_data
    ] if principals_data else []

    titleObject["principals"] = principals

    rating_query = "SELECT averageRating, numVotes FROM ratings WHERE tconst = %s"
    rating_rows = execute_query(rating_query, (titleID,), fetch_data_flag=True, fetch_all_flag=True)
    #rating_row = rating_rows[0]
    for rating_row in rating_rows:
        titleObject["rating"] = {
            "avRating": str(rating_row["averageRating"]),
            "nVotes": str(rating_row["numVotes"])
        }
    return titleObject

def create_name_object(nameID):
    contributor_query = "SELECT * FROM namebasics WHERE nconst = %s"
    contributor_rows = execute_query(contributor_query, (nameID,), fetch_data_flag=True, fetch_all_flag=True)
    contributor_row = contributor_rows[0]
    if not contributor_row:
        return None

    nameObject = {
        "nameID": contributor_row["nconst"],
        "name": contributor_row["primaryName"],
        "namePoster": contributor_row["img_url_asset"],
        "birthYr": str(contributor_row["birthYear"]) if contributor_row["birthYear"] else None,
        "deathYr": str(contributor_row["deathYear"]) if contributor_row["deathYear"] else None,
        "profession": contributor_row["primaryProfession"],
        "nameTitles": []
    }

    titles_query = """
    SELECT pt.tconst, pt.category 
    FROM principals pt
    WHERE pt.nconst = %s
    """
    titles_data = execute_query(titles_query, (nameID,), fetch_data_flag=True, fetch_all_flag=True)
    if titles_data:
        nameObject["nameTitles"] = [{"titleID": row["tconst"], "category": row["category"]} for row in titles_data]

    return nameObject


class get_title(Resource):
    def get(self, titleID):
        title_object = create_title_object(titleID)
        if title_object:
            return title_object, 200
        else:
            return {"message": "Title not found"}, 404

def search_titles_by_title_part(titlePart):
    search_query = """
    SELECT tconst 
    FROM titlebasics 
    WHERE originalTitle LIKE %s
    """
    title_ids = execute_query(search_query, ('%' + titlePart + '%',), fetch_data_flag=True, fetch_all_flag=True)
    if not title_ids:
        return []

    title_objects = [create_title_object(title_id['tconst']) for title_id in title_ids]
    return title_objects

class search_title(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('titlePart', type=str, required=True, location='json')

    def get(self):
        args = self.reqparse.parse_args()
        title_part = args['titlePart']
        title_objects = search_titles_by_title_part(title_part)
        return title_objects, 200 if title_objects else 404

def search_titles_by_genre(qgenre, minrating, yrFrom=None, yrTo=None):
    genre_condition = "FIND_IN_SET(%s, genres)"
    rating_condition = "tconst IN (SELECT tconst FROM ratings WHERE averageRating >= %s)"
    year_condition = "(startYear >= %s AND startYear <= %s)" if yrFrom and yrTo else "1=1"
    
    search_query = f"""
    SELECT tconst
    FROM titlebasics
    WHERE {genre_condition} AND {rating_condition} AND {year_condition}
    """
    values = [qgenre, minrating]
    if yrFrom and yrTo:
        values.extend([yrFrom, yrTo])

    title_ids = execute_query(search_query, values, fetch_data_flag=True, fetch_all_flag=True)

    if not title_ids:
        return []

    title_objects = [create_title_object(title_id['tconst']) for title_id in title_ids]
    return title_objects

class by_genre(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('qgenre', type=str, required=True, location='json')
        self.reqparse.add_argument('minrating', type=str, required=True, location='json')
        self.reqparse.add_argument('yrFrom', type=str, location='json')
        self.reqparse.add_argument('yrTo', type=str, location='json')

    def get(self):
        args = self.reqparse.parse_args()
        title_objects = search_titles_by_genre(args['qgenre'], args['minrating'], args['yrFrom'], args['yrTo'])
        return title_objects, 200 if title_objects else 404

class get_name(Resource):
    def get(self, nameID):
        name_object = create_name_object(nameID)
        if name_object:
            return name_object, 200
        else:
            return {"message": "Contributor not found"}, 404

def search_names_by_name_part(namePart):
    search_query = """
    SELECT nconst
    FROM namebasics
    WHERE primaryName LIKE %s
    """
    professional_ids = execute_query(search_query, ('%' + namePart + '%',), fetch_data_flag=True, fetch_all_flag=True)

    if not professional_ids:
        return []

    name_objects = [create_name_object(professional_id['nconst']) for professional_id in professional_ids]
    return name_objects

class search_name(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('namePart', type=str, required=True, location='json')

    def get(self):
        args = self.reqparse.parse_args()
        name_part = args['namePart']
        name_objects = search_names_by_name_part(name_part)
        return name_objects, 200 if name_objects else 404

def get_top_10_titles_by_genre(genre):
    print("hii")
    search_query = """
    SELECT t.tconst
    FROM titlebasics t
    JOIN ratings r ON t.tconst = r.tconst
    WHERE FIND_IN_SET(%s, t.genres)
    ORDER BY r.averageRating DESC
    LIMIT 10
    """
    title_ids = execute_query(search_query, (genre,), fetch_data_flag=True, fetch_all_flag=True)

    if not title_ids:
        return []

    title_objects = [create_title_object(title_id['tconst']) for title_id in title_ids]
    return title_objects

class top10_by_genre(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('genre', type=str, required=True, location='json')

    def get(self):
        args = self.reqparse.parse_args()
        genre = args['genre']
        top_titles = get_top_10_titles_by_genre(genre)
        return top_titles, 200 if top_titles else 404

api = Api(app, prefix='/ntuaflix_api')

#Διαχειριστικά Endpoints
api.add_resource(health_check, '/admin/healthcheck')
api.add_resource(title_basics, '/admin/upload/titlebasics')
api.add_resource(title_akas, '/admin/upload/titleakas')
api.add_resource(name_basics, '/admin/upload/namebasics')
api.add_resource(title_crew, '/admin/upload/titlecrew')
api.add_resource(title_episode, '/admin/upload/titleepisode')
api.add_resource(title_principal, '/admin/upload/titleprincipals')
api.add_resource(title_ratings, '/admin/upload/titleratings')
api.add_resource(reset_all, '/admin/resetall')

#Λειτουργίες συστήματος
api.add_resource(get_title, '/title/<string:titleID>')
api.add_resource(search_title, '/searchtitle')
api.add_resource(by_genre, '/bygenre')
api.add_resource(get_name, '/name/<string:nameID>')
api.add_resource(search_name, '/searchname')
api.add_resource(top10_by_genre, '/top10bygenre')

if __name__ == "__main__":  
    app.run(debug=True, port='9876')
