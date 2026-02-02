import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

def make_connection():
    """
    Create MySQL database connection
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE'),
            connection_timeout=30
        )

        if connection.is_connected():
            print("Successfully connected to MySQL database")
            return connection
        else:
            print("Failed to connect to MySQL database. Check credentials.")
            return None
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
    
def execute_query(query, params=None, select=True):
    """
    Execute SELECT query and return results
    """
    connection = None
    cursor = None
    try:
        connection = make_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if select:
            result = cursor.fetchall()
            return result

        else:
            connection.commit()
            return True
    
    except Error as e:
        print(f"Query execution error: {e}")
        return None
    
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()