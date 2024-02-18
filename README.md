# SoftEng

NTUA/ECE Software Engineering, 2023-2024

## Introduction

Welcome to the NTUAFlix application repository! This document provides a guide on setting up the repository locally on your computer and running the application. NTUAFlix is a movie streaming platform developed by the NTUA/ECE Software Engineering team for the academic year 2023-2024.

## Prerequisites

Before setting up the repository, ensure the following prerequisites are met:
- MySQL is installed and configured on your system.
- Python is installed on your system.

## Setup Instructions

Follow these steps to set up the git repository:

1. **Clone the Repository**: 
   - Clone the git repository to your local machine using the command:
     ```
     git clone <repository_url>
     ```
   
2. **Install Dependencies**:
   - Navigate to the `util` folder and run the `dependencies.py` file to install all necessary dependencies:
     ```
     cd util
     python dependencies.py
     ```

3. **Database Setup**:
   - Run the `setup.py` file at the top-level directory of the repository to set up the database and initialize the application:
     ```
     python setup.py
     ```

4. **Run the Server**:
   - Navigate to the `front-end` folder and run the `server.py` file to start the server:
     ```
     cd front-end
     python server.py
     ```

5. **Access the Application**:
   - Once the server is running, you can access the NTUAFlix application at [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

## Additional Information

- The NTUAFlix application is built using Python and MySQL.
- The `dependencies.py` file contains all necessary functions for installing dependencies.
- The `setup.py` file initializes the database and starts the API server.
- The `server.py` file in the `front-end` folder launches the front-end server.
- Ensure to have a stable internet connection during setup to download necessary dependencies.
  
For any issues or inquiries, please contact the project maintainers. 

Happy streaming! 🎬🍿
