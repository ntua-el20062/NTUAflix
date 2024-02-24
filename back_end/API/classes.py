from flask import request, jsonify, make_response, session
from functools import wraps
from flask_restful import Api, Resource, reqparse
import json, jwt, datetime
from flask_mysqldb import MySQL
from back_end.API import db
import csv
import pymysql
import os
import sqlparse
import mysql.connector

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ functions @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def edit_file(table, tsv_data, data_types):
    # Parse the TSV data
    rows = csv.reader(tsv_data.splitlines(), delimiter='\t')
    headers = next(rows)
        
    data = []
    for row in rows:
        entry = {}
        for header, value in zip(headers, row):
            if value == r'\N' or not value:
                entry[header] = None
            else:
                try:
                    data_type = data_types.get(header, str)
                    if data_type == int:
                        entry[header] = int(value)
                    elif data_type == float:
                        entry[header] = float(value)
                    else:
                        entry[header] = value.strip()
                except ValueError as e:
                    # Log the error and skip this row or handle it as needed
                    print(f"Error converting value '{value}' in column '{header}': {e}")
                    continue  # Skip this row
        data.append(entry)

    if not data:
        return {"status": "No data to insert"}, 204

    # Insert data into database
    keys = data[0].keys()
    columns = ', '.join(keys)
    placeholders = ', '.join(['%s'] * len(keys))
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    values = [tuple(row[key] for key in keys) for row in data]

    cur = db.get_db().cursor()
    cur.executemany(query, values)
    db.get_db().commit()
    cur.close()

    return {"status": f"{table} data added"}, 200

def clear_database():
    try:
        conn = db.get_db()
        cur = conn.cursor()
        # List of tables to clear
        tables = ['ratings', 'episode', 'crew', 'akas', 'titlebasics', 'principals', 'namebasics']
        cur.execute(f"SET FOREIGN_KEY_CHECKS = 0;")
        for table in tables:
            cur.execute(f"DELETE FROM {table}")
        cur.execute(f"SET FOREIGN_KEY_CHECKS = 1;")
        conn.commit()
    except pymysql.MySQLError as e:
            # Handle MySQL errors
            return {"this error": str(e)}, 500
    except Exception as e:
            # Handle any other exceptions
            return {"that error": str(e)}, 500
    finally:
        cur.close()

def split_sql_statements(sql_script):
    statements = sqlparse.split(sql_script)
    return [str(statement) for statement in statements if statement.strip()]


def execute_sql_file(sql_file_path):
    try:
        db_conn = db.get_db()
        cur = db_conn.cursor()

        # Read SQL script
        try:
            with open(sql_file_path, 'r', encoding='utf-8') as file:
                 sql_script = file.read()
        except FileNotFoundError:
            return {"error": "SQL file not found"}, 404
        except Exception as e:
            return {"error": f"Error while opening SQL file: {str(e)}"}, 500

        # Split script into individual statements
        statements = split_sql_statements(sql_script)

        # Execute each statement
        for statement in statements:
            if statement.strip():
                # Ignore empty statements
                try:
                    cur.execute(statement)
                except pymysql.Error as e:
                    # Handle MySQL errors
                    db_conn.rollback()
                    return {"error": f"MySQL Error: {str(e)}"}, 500

        # Commit changes
        db_conn.commit()
        cur.close()
        return {"status": "Database repopulated successfully"}, 200

    except Exception as e:
        # Handle any other exceptions
        return {"error": f"Unexpected Error: {str(e)}"}, 500
    
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


#@@@@@@@@@@@@@@@ Classes @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


########################## Διαχειριστικές Απαιτήσεις ##################################
#######################################################################################

class health_check(Resource):
    def get(self):
        # Example database check (modify as per your setup)
        try:
            cur = db.get_db().cursor()
            cur.execute("SELECT 1")
            cur.close()
            db_status = "Connected"
        except Exception as e:
            db_status = f"Error: {e}"

        return {"status": "OK", "database": db_status}, 200

#κάτι τέτοιο πρέπει να κάνετε για όλα τα insertions
class title_basics(Resource):
    def post(self):
        # Define the data types for each column
        title_basics_types = {
            "tconst": str,
            "titleType": str,
            "primaryTitle": str,
            "originalTitle": str,
            "isAdult": int,
            "startYear": int,
            "endYear": int,
            "runtimeMinutes": int,
            "genres": str,
            "img_url_asset": str
        }              
        
        file = request.files.get("tsv_title_basics")
        tsv_title_basics = file.read().decode('utf-8')      
        try:
            # Attempt to edit the file
            result = edit_file("titlebasics", tsv_title_basics, title_basics_types)
            return(result)
        except Exception as e:
            # Check if the error is related to an unknown column
            if "Unknown column" in str(e):
                # Return a custom response with a 400 status code
                return {"error": "Unknown column in database"}, 400
            else:
                # For other errors, return a generic 500 error
                return {"error": "Internal server error"}, 500


class title_akas(Resource):
    def post(self):
    # Define the data types for each column
        aka_types = {
            "titleId": str,
            "ordering": int,
            "title": str,
            "region": str,
            "language": str,
            "type": str,
            "attributes": str,
            "isOriginalTitle": int
        }

        file = request.files.get("tsv_aka")
        tsv_aka = file.read().decode('utf-8')        

        # Check if tsv_data is provided
        try:
            result = edit_file("akas", tsv_aka, aka_types)
            return(result)
        except Exception as e:
            # Check if the error is related to an unknown column
            if "Unknown column" in str(e):
                # Return a custom response with a 400 status code
                return {"error": "Unknown column in database"}, 400
            else:
                # For other errors, return a generic 500 error
                return {"error": "Internal server error"}, 500

class name_basics(Resource):
    def post(self):
    # Define the data types for each column
        professionals_types = {
            "nconst": str,
            "primaryName": str,
            "birthYear": int,
            "deathYear": int,
            "primaryProfession": str,
            "knownForTitles": str,
            "img_url_asset": str
            }
        
        file = request.files.get("tsv_name_basics")
        tsv_name_basics= file.read().decode('utf-8')        
        try:
            result = edit_file("namebasics", tsv_name_basics, professionals_types)
            return(result)
        except Exception as e:
            # Check if the error is related to an unknown column
            if "Unknown column" in str(e):
                # Return a custom response with a 400 status code
                return {"error": "Unknown column in database"}, 400
            else:
                # For other errors, return a generic 500 error
                return {"error": "Internal server error"}, 500

class title_crew(Resource):
    def post(self):
    # Define the data types for each column
        title_crew_types = {
            "tconst": str,
            "directors": str,
            "writers": str
            }

        file = request.files.get("tsv_title_crew")
        tsv_title_crew= file.read().decode('utf-8')        

        try:
            result = edit_file("crew", tsv_title_crew, title_crew_types)
            return(result)
        except Exception as e:
            # Check if the error is related to an unknown column
            if "Unknown column" in str(e):
                # Return a custom response with a 400 status code
                return {"error": "Unknown column in database"}, 400
            else:
                # For other errors, return a generic 500 error
                return {"error": "Internal server error"}, 500

        
class title_episode(Resource):
    def post(self):
    # Define the data types for each column
        title_episode_types = {
            "tconst": str,
            "parentTconst": str,
            "seasonNumber": int,
            "episodeNumber": int
            }

        file = request.files.get("tsv_title_episode")
        tsv_title_episode= file.read().decode('utf-8')        

        # Check if tsv_data is provided
        try: 
            result = edit_file("episode", tsv_title_episode, title_episode_types)
            return(result)
        except Exception as e:
            # Check if the error is related to an unknown column
            if "Unknown column" in str(e):
                # Return a custom response with a 400 status code
                return {"error": "Unknown column in database"}, 400
            else:
                # For other errors, return a generic 500 error
                return {"error": "Internal server error"}, 500

class title_principal(Resource):
    def post(self):
        title_principal_types = {
            "tconst": str,
            "ordering": int,
            "nconst": str,
            "category": str,
            "job": str,
            "characters": str,
            "img_url_asset": str
            }
         
        file = request.files.get("tsv_title_principal")
        tsv_title_principal= file.read().decode('utf-8')        

        try:
            result = edit_file("principals", tsv_title_principal, title_principal_types)
            return(result)
        except Exception as e:
            # Check if the error is related to an unknown column
            if "Unknown column" in str(e):
                # Return a custom response with a 400 status code
                return {"error": "Unknown column in database"}, 400
            else:
                # For other errors, return a generic 500 error
                return {"error": "Internal server error"}, 500

class title_ratings(Resource):
    def post(self):
        title_ratings_types = {
            "tconst": str,
            "averageRating": float,
            "numVotes": int
            }
        
        file = request.files.get("tsv_title_ratings")
        tsv_title_ratings= file.read().decode('utf-8')        

        try: 
            result = edit_file("ratings", tsv_title_ratings, title_ratings_types)
            return(result)
        except Exception as e:
            # Check if the error is related to an unknown column
            if "Unknown column" in str(e):
                # Return a custom response with a 400 status code
                return {"error": "Unknown column in database"}, 400
            else:
                # For other errors, return a generic 500 error
                return {"error": "Internal server error"}, 500

class reset_all(Resource):
    def post(self):
        print(os.listdir('C:\\temp\\softeng23-05\\softeng23-05\\back_end'))
        sql_file_path = './back_end/ntuaflix_insert.sql'  # Path to your SQL file
        try:
            clear_database()
            return execute_sql_file(sql_file_path)
        except Exception as e:
            return {"error": str(e)}, 500


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
        "runtimeMinutes": str(title_row["runtimeMinutes"]),

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

    if not contributor_rows:
        return None

    contributor_row = contributor_rows[0]


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

def get_top_10_titles_by_genre():
    genres_query = "SELECT DISTINCT genres FROM titlebasics"
    all_genres = execute_query(genres_query, None, fetch_data_flag=True, fetch_all_flag=True)
    if not all_genres:
        return {}


    unique_genres = set(
        genre.strip()
        for genres_field in all_genres
        if genres_field['genres'] is not None  # Add this check
        for genre in genres_field['genres'].split(',') if genre.strip()
    )
    top_titles_by_genre = {}
    for genre in unique_genres:
        search_query = """
        SELECT t.tconst
        FROM titlebasics t
        JOIN ratings r ON t.tconst = r.tconst
        WHERE FIND_IN_SET(%s, t.genres)
        ORDER BY r.averageRating DESC
        LIMIT 10
        """
        title_ids = execute_query(search_query, (genre,), fetch_data_flag=True, fetch_all_flag=True)
        if title_ids:
            top_titles_by_genre[genre] = [create_title_object(title_id['tconst']) for title_id in title_ids]
    return top_titles_by_genre

class top10_by_genre(Resource):
    def get(self):
        top_titles = get_top_10_titles_by_genre()
        return top_titles, 200 if top_titles else 404

