import subprocess

def install_packages():
    packages = [
        'Flask',
        'Flask-RESTful',
        'Flask-MySQLdb',
        'pymysql',
        'sqlparse',
        'mysql-connector-python',
        'Flask-RESTful',
        'Flask-MySQL',
    ]

    for package in packages:
        try:
            subprocess.check_call(['pip', 'install', package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}. Error: {e}")

if __name__ == "__main__":
    install_packages()