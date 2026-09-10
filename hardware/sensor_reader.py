import random
from database.models import create_ecg_record, create_ppg_record, create_mpu6050_record, create_temperature_record


def read_ecg(device_id):
    """
    Simulates reading ECG data from AD8232 sensor.
    In production, replace with actual I2C/ADC read.

    Args:
        device_id (str): Device identifier

    Returns:
        dict: Record with timestamp, device_id, and ecg_voltage
    """
    # Simulate ECG voltage between -0.5 and 0.5 volts
    simulated_voltage = random.uniform(-0.5, 0.5)
    record = create_ecg_record(device_id, simulated_voltage)
    return record


def read_ppg(device_id):
    """
    Simulates reading PPG data from MAX30102 sensor.
    In production, replace with actual I2C read.

    Args:
        device_id (str): Device identifier

    Returns:
        dict: Record with timestamp, device_id, ppg_ir, and ppg_red
    """
    # Simulate PPG infrared and red light values (0-65535 range)
    simulated_ir = random.randint(40000, 50000)
    simulated_red = random.randint(38000, 48000)
    record = create_ppg_record(device_id, simulated_ir, simulated_red)
    return record


def read_mpu6050(device_id):
    """
    Simulates reading motion data from MPU6050 sensor.
    In production, replace with actual I2C read.

    Args:
        device_id (str): Device identifier

    Returns:
        dict: Record with timestamp, device_id, acceleration_x, acceleration_y, acceleration_z
    """
    # Simulate acceleration on X, Y, Z axes (in g)
    simulated_x = random.uniform(-0.5, 0.5)
    simulated_y = random.uniform(-0.5, 0.5)
    simulated_z = random.uniform(9.5, 10.1)  # Near gravity when stationary
    record = create_mpu6050_record(device_id, simulated_x, simulated_y, simulated_z)
    return record


def read_temperature(device_id):
    """
    Simulates reading temperature data from GY-906 sensor.
    In production, replace with actual I2C read.

    Args:
        device_id (str): Device identifier

    Returns:
        dict: Record with timestamp, device_id, and temperature_c
    """
    # Simulate body temperature (36-38°C is normal)
    simulated_temp = random.uniform(36.0, 37.5)
    record = create_temperature_record(device_id, simulated_temp)
    return record


def read_all_sensors(device_id):
    """
    Reads all sensors and returns a dictionary of all records.
    Useful for collecting all data in one call.

    Args:
        device_id (str): Device identifier

    Returns:
        dict: Dictionary with keys 'ecg', 'ppg', 'mpu6050', 'temperature'
    """
    return {
        "ecg": read_ecg(device_id),
        "ppg": read_ppg(device_id),
        "mpu6050": read_mpu6050(device_id),
        "temperature": read_temperature(device_id)
    }
