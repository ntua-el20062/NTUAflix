import subprocess
import sys

def install_dependencies():
    dependencies = [
        'pymysql',
        'sqlparse',
        'Flask',
        'Flask-RESTful',
        'Flask-MySQLdb',
        'Flask-Login',
        'Flask-WTF',
        'Flask-MySQL',
        'mysqlclient',
        'PyJWT',
        'mysql-connector-python',
    ]

    for package in dependencies:
        install_package(package)

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}")

# if __name__ == "__main__":
#     install_dependencies()

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