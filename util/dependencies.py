import subprocess
import sys

def install_dependencies():
    dependencies = [
        'pymysql == 1.1.0',
        'sqlparse == 0.4.4',
        'Flask == 2.3.3',
        'Flask-RESTful == 0.3.10',
        'Flask-MySQLdb == 2.2.4',
        'Flask-Login == 0.6.3',
        'Flask-WTF == 1.2.1',
        'Flask-MySQL == 1.5.2',
        'mysqlclient == 2.2.1',
        'PyJWT == 2.8.0',
        'mysql-connector-python == 8.2.0',
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
