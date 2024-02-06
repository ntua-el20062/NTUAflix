import threading
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
import time

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '161809'
MYSQL_DATABASE = 'ntuaflix'

DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
metadata = MetaData()

title_basics_table = Table('titlebasics', metadata, autoload_with=engine)

Session = sessionmaker(bind=engine)
start_time = time.time()

successful_requests_lock = threading.Lock()
successful_requests = 0

def simulate_select_operation(session):
    try:
        query = select(title_basics_table)
        start_time = time.time()
        result = session.execute(query)
        end_time = time.time()
        session.commit()
        print(f"Request completed in {end_time - start_time:.4f} seconds")

        with successful_requests_lock:
            global successful_requests
            successful_requests += 1

    except Exception as e:
        print(f"Error during SELECT operation: {e}")
        session.rollback()

def simulate_request(session):
    try:
        simulate_select_operation(session)
    except Exception as e:
        print(f"Error during request: {e}")

if __name__ == "__main__":
    request_count = 2000 # can be increased up to 4k with not many unsuccesful requests and it takes aprox. 13 sec for 2k which is more than enough for our app
    threads = []

    # Create a single engine and session for all threads
    engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
    metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    for _ in range(request_count):
        thread = threading.Thread(target=simulate_request, args=(Session(),))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # Close the engine
    engine.dispose()

    elapsed_time = time.time() - start_time
    print(f"Total time elapsed: {elapsed_time:.2f} seconds")
    print(f"Number of successful requests: {successful_requests} out of {request_count} total requests")
