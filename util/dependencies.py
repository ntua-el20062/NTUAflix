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