import mysql.connector

# Database connection parameters for MySQL
db_params = {
    'host': 'localhost',
    'port': 3306,
    'database': 'ntuaflix',
    'user': 'root',
    'password': '161809',
}

def test_unauthorized_access():
    connection = None

    try:
        # Try to connect to the MySQL database with incorrect credentials
        connection = mysql.connector.connect(
            host=db_params['host'],
            port=db_params['port'],
            database=db_params['database'],
            user='root',
            password='262901',
        )

    except mysql.connector.Error as e:
        # print(f"Error: {e}")
        print("Connected to the database - Unauthorized access!")

    finally:
        if connection:
            connection.close()

def test_authorized_access():
    connection = None

    try:
        # Connect to the MySQL database with correct credentials
        connection = mysql.connector.connect(**db_params)
        print("Connected to the database - Authorized access!")

        # Perform authorized operations here, if needed

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        if connection:
            connection.close()
def execute_query(query, params=None, expected_results=None):
    try:
        # Connect to the database
        with mysql.connector.connect(**db_params) as connection:
            # Create a cursor
            with connection.cursor() as cursor:
                # Execute the query with parameters
                if params is not None:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                # Fetch results
                results = cursor.fetchall()

                # Validate the results
                if expected_results is not None and results != expected_results:
                    print("Test failed: Unexpected results.")
                    print(f"Expected: {expected_results}")
                    print(f"Actual: {results}")
                else:
                    print("Test passed: Results are as expected.")

                # Commit the transaction
                connection.commit()

    except Exception as e:
        print(f"Error: {e}")

# Example usage with expected results
if __name__ == "__main__":
    # Example complex query with parameterized genre
    complex_query_top10 = """
    SELECT t.tconst, t.primaryTitle, r.averageRating
        FROM titlebasics t
        JOIN ratings r ON t.tconst = r.tconst
        WHERE t.genres = %s
        ORDER BY r.averageRating DESC, t.primaryTitle ASC
        LIMIT 10
    """
    complex_query1 = """
    SELECT 
        tb.tconst,
        tb.primaryTitle,
        tb.startYear,
        r.averageRating
    FROM 
        titlebasics tb
    JOIN 
        ratings r ON tb.tconst = r.tconst
    JOIN 
        principals p ON tb.tconst = p.tconst
    JOIN 
        namebasics nb ON p.nconst = nb.nconst
    WHERE 
        tb.titleType = 'movie'
        AND tb.startYear >= 1950
        AND r.numVotes > 100
    GROUP BY 
        tb.tconst
    HAVING 
        COUNT(DISTINCT nb.nconst) >= 3
    ORDER BY 
        r.averageRating DESC, 
        tb.primaryTitle ASC
    LIMIT 10;
    """
    complex_query2 = """
   WITH RankedMovies AS (
    SELECT
        tb.tconst,
        tb.primaryTitle,
        tb.startYear,
        tb.genres,
        ratings.averageRating,
        ROW_NUMBER() OVER(PARTITION BY tb.genres ORDER BY ratings.averageRating DESC, tb.primaryTitle) AS genre_rank
    FROM
        titlebasics tb
    JOIN ratings ON tb.tconst = ratings.tconst
    WHERE
        tb.titleType = 'movie'
    AND tb.startYear BETWEEN 1991 AND 2022
),
GenreStats AS (
    SELECT
        genres,
        COUNT(*) AS num_movies
    FROM
        RankedMovies
    GROUP BY
        genres
    HAVING
        COUNT(*) > 1
)
SELECT
    rm.tconst,
    rm.primaryTitle,
    rm.startYear,
    rm.genres,
    rm.averageRating
FROM
    RankedMovies rm
JOIN GenreStats gs ON rm.genres = gs.genres
WHERE
    rm.genre_rank = 1
ORDER BY
    rm.genres, rm.averageRating DESC, rm.primaryTitle ASC;

    """
    complex_query3 = """
        WITH top_directors AS (
            SELECT nconst, primaryName
            FROM namebasics
            WHERE nconst IN (
                SELECT nconst
                FROM principals
                WHERE category = 'director'
                GROUP BY nconst
                HAVING COUNT(DISTINCT tconst) > 3
            )
        )

        SELECT titlebasics.tconst, titlebasics.primaryTitle, titlebasics.startYear, titlebasics.genres,
            ratings.averageRating, ratings.numVotes,
            top_directors.primaryName AS director_name,
            GROUP_CONCAT(DISTINCT crew.writers) AS writer_names
        FROM titlebasics
        JOIN ratings ON titlebasics.tconst = ratings.tconst
        JOIN crew ON titlebasics.tconst = crew.tconst
        JOIN top_directors ON crew.directors = top_directors.nconst
        WHERE titlebasics.titleType = 'movie'
            AND titlebasics.startYear BETWEEN 1900 AND 2024
            AND ratings.numVotes > 300
        GROUP BY titlebasics.tconst
        HAVING COUNT(DISTINCT crew.writers) > 1
        ORDER BY ratings.averageRating DESC, ratings.numVotes DESC
        LIMIT 10;
    """


    # Define expected results for the test
    expected_results_drama = [
        ('tt0102281', 'The Law Lord', 8.3),
        ('tt0101894', 'Flea Bites', 8.2),
        ('tt0098542', 'Ti, koyto si na nebeto', 8.2),
        ('tt0099032', 'Amongst Barbarians', 8.0),
        ('tt0073481', 'Old Times', 8.0),
        ('tt0100642', 'Small Zones', 8.0),
        ('tt0096135', 'Sometime in August', 8.0),
        ('tt0096752', 'Abrahams Gold', 7.9),
        ('tt0101972', 'The Grass Arena', 7.9),
        ('tt0099003', 'Aimée', 7.7)
    ]
    expected_results_action = [
        ('tt0097506', 'High Score', 5.8),
        ('tt0095290', 'Lethal Angels', 5.7),
        ('tt0097542', 'The Trace of Lynx', 5.4),
        ('tt0094926', 'Curse of the Crystal Eye', 4.8),
        ('tt0096837', 'The Assassin', 4.6),
        ('tt0098422', 'The Sword of Bushido', 4.5),
        ('tt0095335', 'The Vengeance', 4.3),
        ('tt0097004', 'Caged Fury', 4.0),
        ('tt0092926', 'Dragon Hunt', 3.0)
    ]
    expected_results_comedy = [
        ('tt0095469', 'King of Stanley Market', 6.5), 
        ('tt0098244', 'Saturday, Sunday and Monday', 6.4),
        ('tt0097111', 'Go to Work, Vagabond II', 6.3),  
        ('tt0098294', 'La settimana della sfinge', 6.3),
        ('tt0099542', 'A Family for Joe', 6.2),  
        ('tt0091899', 'The Scarlet Scorpion', 6.2),  
        ('tt0096859', "L'avaro", 6.0), 
        ('tt0097644', 'Kapital, czyli jak zrobic pieniadze w Polsce', 5.8), 
        ('tt0099038', 'Anekdoty', 5.6),
        ('tt0097525', 'Hopnick', 5.6), 
     ]
    expected_results1 = [
        ('tt0097851', 'Mathilukal', 1990 ,8.3),
        ('tt0099028', 'American Dream', 1990, 7.8),
        ('tt0095111', 'The Escape', 1991, 7.8),
        ('tt0098999', 'Agneepath', 1990, 7.6),
        ('tt0097253', 'Deja vu', 1990, 7.5),
        ('tt0097848', 'Mother', 1990, 7.5),
        ('tt0098532', 'The Match Factory Girl', 1990, 7.5),
        ('tt0092507', 'Abhimanyu', 1991, 7.3),
        ('tt0093572', 'Moskovskaya elegiya', 1990, 7.3),
        ('tt0097062', 'Chyornaya roza - emblema pechali, krasnaya roza - emblema lyubvi', 1990, 7.2)
    ]
    expected_results2 = [
        ('tt0096397', 'Vita da cane', 1992, '', 6.0), 
        ('tt0094926', 'Curse of the Crystal Eye', 1991, 'Action', 4.8), 
        ('tt0088267', 'An Eternal Combat', 1991, 'Action,Comedy,Fantasy', 5.5), 
        ('tt0077432', 'Bloody Hero', 1991, 'Action,Drama', 5.4), 
        ('tt0095394', 'Jericho', 1991, 'Adventure,Drama', 7.1), 
        ('tt0095469', 'King of Stanley Market', 1998, 'Comedy', 6.5), 
        ('tt0084015', 'Goodbye Paradise', 1991, 'Drama', 7.3), 
        ('tt0094841', 'The House of Smiles', 1991, 'Drama,Romance', 6.5), 
        ('tt0094900', 'Committed', 1991, 'Drama,Thriller', 5.0)
    ]
    expected_results3=[]


    # Test unauthorized access
    test_unauthorized_access()

    # Test authorized access
    test_authorized_access()
    # Execute the complex query with the specified genre
    execute_query(complex_query_top10, ('Drama',), expected_results_drama)
    execute_query(complex_query_top10, ('Action',), expected_results_action)
    execute_query(complex_query_top10, ('Comedy',), expected_results_comedy)
    execute_query(complex_query1, expected_results=expected_results1)
    execute_query(complex_query2, expected_results=expected_results2)
    execute_query(complex_query3, expected_results=expected_results3)

    
    

    



