import sys
import os
import psycopg2
from psycopg2 import sql

# Add parent directory to path so we can import config.py from root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import DATABASE_URL, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT


def get_db_connection():
    """
    Creates and returns a connection to PostgreSQL database.
    Uses credentials from .env file (loaded through config.py)

    Returns:
        psycopg2 connection object
    """
    connection = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )
    return connection


def execute_query(query, params=None):
    """
    Executes a SQL SELECT query and returns results.

    Args:
        query (str): SQL query string (e.g., "SELECT * FROM ecg_data WHERE device_id = %s")
        params (tuple, optional): Tuple of parameters to safely insert into query (prevents SQL injection)

    Returns:
        list or None: List of tuples (rows) returned by query, or None if error
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Execute query with parameters
        cursor.execute(query, params)
        # Fetch all results
        result = cursor.fetchall()
        # Commit the transaction
        connection.commit()
        return result
    except Exception as e:
        # If error, rollback changes
        connection.rollback()
        print(f"Database error: {e}")
        return None
    finally:
        # Always close cursor and connection
        cursor.close()
        connection.close()


def insert_sensor_data(table_name, data):
    """
    Inserts a row of sensor data into the specified table.
    Safely handles column names and values to prevent SQL injection.

    Args:
        table_name (str): Name of table (e.g., "ecg_data", "ppg_data", "mpu6050_data", "temperature_data")
        data (dict): Dictionary of column names and values
                     Example: {
                         "timestamp": "2026-09-09 12:30:45+00:00",
                         "device_id": "driver_001",
                         "ecg_voltage": 0.85
                     }

    Returns:
        bool: True if insert successful, False if error
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Extract column names and values from dictionary
        columns = list(data.keys())
        values = list(data.values())

        # Build SQL query safely using sql module
        # This prevents SQL injection attacks
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),  # Table name (safe)
            sql.SQL(", ").join(map(sql.Identifier, columns)),  # Column names (safe)
            sql.SQL(", ").join(sql.Placeholder() * len(columns))  # Placeholders for values
        )

        # Execute the query with values as parameters
        cursor.execute(query, values)
        # Commit the transaction (save to database)
        connection.commit()
        print(f"Successfully inserted data into {table_name}")
        return True
    except Exception as e:
        # If error, undo any changes
        connection.rollback()
        print(f"Insert error: {e}")
        return False
    finally:
        # Always close cursor and connection
        cursor.close()
        connection.close()


def fetch_sensor_data(table_name, device_id, limit=100):
    """
    Fetches sensor data for a specific device from the specified table.

    Args:
        table_name (str): Name of sensor table (e.g., "ecg_data", "ppg_data")
        device_id (str): Device identifier (e.g., "driver_001")
        limit (int, optional): Maximum number of rows to return (default: 100)

    Returns:
        list or None: List of tuples (rows) matching the criteria, or None if error
    """
    query = "SELECT * FROM {} WHERE device_id = %s ORDER BY timestamp DESC LIMIT %s".format(table_name)
    return execute_query(query, (device_id, limit))


def close_connection(connection):
    """
    Safely closes a database connection.

    Args:
        connection (psycopg2 connection): The connection object to close

    Returns:
        bool: True if closed successfully, False if error
    """
    try:
        if connection is not None:
            connection.close()
            print("Database connection closed")
            return True
    except Exception as e:
        print(f"Error closing connection: {e}")
        return False
