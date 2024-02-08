from flask import Flask
from flaskext.mysql import MySQL
import pymysql
from flask_restful import Api
from back_end.API import app
from back_end.API.classes import *

api = Api(app, prefix='/ntuaflix_api')

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found"}), 404

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

# if __name__ == "__main__":  
#     app.run(debug=True, port=9876)
