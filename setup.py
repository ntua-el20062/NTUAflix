#Install dependencies, setup database, run the API server, run the webserver
from util.dependencies import install_dependencies

# Install all dependencies
install_dependencies()

import pymysql
import sys
import sqlparse
from back_end.API.main import app  # Adjusted import statement


def split_sql_statements(sql_script):
    statements = sqlparse.split(sql_script)
    return [str(statement) for statement in statements if statement.strip()]

def execute_sql_create_file(cursor, file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        commands = split_sql_statements(sql_script)
        for command in commands:
            if command.strip():
                #print(f"Executing SQL command: {command}")  # Debug print
                cursor.execute(command)
    except FileNotFoundError:
        print(f"SQL file not found: {file_path}")
        return {"error": f"SQL file not found: {file_path}"}
    except UnicodeDecodeError:
        print(f"Unicode decode error in file: {file_path}")
        return {"error": f"Unicode decode error in file: {file_path}"}
    except pymysql.MySQLError as e:
        print(f"Error executing SQL command: {e}")
        return {"error": f"Error executing SQL command: {e}"}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": f"Unexpected error: {e}"}
    return {"status": "SQL file executed successfully"}


def database_exists(host, user, password, db_name):
    conn = None
    try:
        conn = pymysql.connect(host=host, user=user, passwd=password)
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        for database in cursor:
            if db_name in database:
                return True
        return False
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL Server: {e}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()

def create_and_initialize_database(host, user, password, db_name):
    try:
        conn = pymysql.connect(host=host, user=user, passwd=password)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created successfully.")
        
        # Switch to the newly created database
        conn.select_db(db_name)

        # Execute SQL files
        response = execute_sql_create_file(cursor, './back_end/ntuaflix_schema.sql')
        if "error" in response:
            print(response["error"])
            sys.exit(1)
            
        response = execute_sql_create_file(cursor, './back_end/ntuaflix_insert.sql')
        if "error" in response:
            print(response["error"])
            sys.exit(1)
        
        conn.commit()

        print("Database initialized successfully.")
    except pymysql.MySQLError as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # Database configuration
    host = "127.0.0.1"
    user = "root"
    password = ""
    db_name = "ntuaflix"

    # Check if the database exists
    if not database_exists(host, user, password, db_name):
        # Create and initialize the database if it does not exist
        create_and_initialize_database(host, user, password, db_name)

    # Start the API server
    app.run(debug=True, port=9876)
