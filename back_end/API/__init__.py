from flask import Flask
from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__)

app.config["SECRET_KEY"] = "SECRET_KEY"
app.config["MYSQL_DB"] = "ntuaflix"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_HOST"] = "127.0.0.1"

db = MySQL(app,
           prefix="ntuaflix",
           host="localhost",
           user="root",
           db="ntuaflix",
           cursorclass=pymysql.cursors.DictCursor
           )

db.init_app(app)