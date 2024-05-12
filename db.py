import os
import pymysql

def db_connection():
    """
    Establishes a connection to the database using environment variables for configuration.

    Returns:
        pymysql.connections.Connection: The database connection object.
    """
    conn = None
    try:
        conn = pymysql.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            database=os.environ.get('DB_DATABASE'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as e:
        print(e)
    return conn

def create_table():
    """
    Creates the 'books' table in the database if it does not already exist.
    """
    conn = db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT 1 FROM books LIMIT 1")
    except pymysql.Error:
        sql_schema = """
            CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            publisher VARCHAR(255) NOT NULL,
            language VARCHAR(255) NOT NULL  
            )
        """
        cursor.execute(sql_schema)
        conn.commit()
    finally:
        conn.close()
