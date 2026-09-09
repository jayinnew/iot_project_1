import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# DATABASE CONFIGURATION
DATABASE_URL = os.getenv('DATABASE_URL')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# FLASK CONFIGURATION
FLASK_ENV = os.getenv('FLASK_ENV')
FLASK_DEBUG = os.getenv('FLASK_DEBUG') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')
API_HOST = os.getenv('API_HOST')
API_PORT = int(os.getenv('API_PORT'))

# HARDWARE/SENSOR CONFIGURATION
SENSOR_SAMPLE_RATE = int(os.getenv('SENSOR_SAMPLE_RATE'))
ECG_ENABLED = os.getenv('ECG_ENABLED') == 'True'
PPG_ENABLED = os.getenv('PPG_ENABLED') == 'True'
MPU6050_ENABLED = os.getenv('MPU6050_ENABLED') == 'True'
TEMP_SENSOR_ENABLED = os.getenv('TEMP_SENSOR_ENABLED') == 'True'

# LOGGING CONFIGURATION
LOG_LEVEL = os.getenv('LOG_LEVEL')
LOG_FILE = os.getenv('LOG_FILE')
