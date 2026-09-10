import sys
import os

# Add parent directory to path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_connection import insert_sensor_data as db_insert


def validate_sensor_data(table_name, data):
    """
    Validates sensor data before inserting into database.
    Checks if values are within expected ranges for each sensor type.

    Args:
        table_name (str): Name of table (ecg_data, ppg_data, mpu6050_data, temperature_data)
        data (dict): Sensor data dictionary to validate

    Returns:
        tuple: (is_valid: bool, error_message: str or None)
               - is_valid: True if data passes validation, False if it fails
               - error_message: Description of the validation error, or None if valid
    """
    # Define validation rules for each sensor type
    # Each rule specifies min and max acceptable values
    validation_rules = {
        'ecg_data': {
            'ecg_voltage': {'min': -1.0, 'max': 1.0}
            # ECG voltage should be between -1.0 and 1.0 volts
        },
        'ppg_data': {
            'ppg_ir': {'min': 0, 'max': 65535},
            # Infrared light intensity: 0 to 65535 (16-bit unsigned)
            'ppg_red': {'min': 0, 'max': 65535}
            # Red light intensity: 0 to 65535 (16-bit unsigned)
        },
        'mpu6050_data': {
            'acceleration_x': {'min': -16.0, 'max': 16.0},
            # X-axis acceleration: -16 to 16g
            'acceleration_y': {'min': -16.0, 'max': 16.0},
            # Y-axis acceleration: -16 to 16g
            'acceleration_z': {'min': -16.0, 'max': 16.0}
            # Z-axis acceleration: -16 to 16g
        },
        'temperature_data': {
            'temperature_c': {'min': 20.0, 'max': 45.0}
            # Body temperature: 20 to 45 degrees Celsius
        }
    }

    # Check if this table has validation rules defined
    if table_name not in validation_rules:
        # No rules for this table, so it's valid
        return True, None

    # Get the validation rules for this table
    rules = validation_rules[table_name]

    # Check each field that should be in the data
    for field, limits in rules.items():
        # Check if the field exists in the data
        if field not in data:
            error_msg = f"Missing field: {field}"
            return False, error_msg

        # Get the value from data
        value = data[field]

        # Check if value is within acceptable range
        if value < limits['min'] or value > limits['max']:
            error_msg = f"{field} out of range: {value} (expected {limits['min']} to {limits['max']})"
            return False, error_msg

    # All validations passed
    return True, None


def insert_sensor_data(table_name, data):
    """
    Inserts sensor data into the correct database table.
    Validates data, then calls db_connection.py to insert into PostgreSQL.

    Args:
        table_name (str): Name of table (ecg_data, ppg_data, mpu6050_data, temperature_data)
                         Comes from mqtt_subscriber.py
        data (dict): Sensor data dictionary
                    Example: {"timestamp": "2026-09-10T10:00:14Z", "device_id": "driver_001", "ecg_voltage": 0.85}

    Returns:
        bool: True if successful, False if failed
    """
    try:
        # Step 1: Validate the data
        is_valid, error_msg = validate_sensor_data(table_name, data)

        if not is_valid:
            print(f"✗ Validation failed for {table_name}: {error_msg}")
            print(f"  Data received: {data}")
            return False

        # Step 2: Insert into database using db_connection.py
        # db_insert is the insert_sensor_data function from db_connection.py
        result = db_insert(table_name, data)

        if result:
            print(f"✓ Successfully inserted into {table_name}")
            return True
        else:
            print(f"✗ Failed to insert into {table_name}")
            return False

    except Exception as e:
        print(f"✗ Error inserting into {table_name}: {e}")
        import traceback
        traceback.print_exc()
        return False
