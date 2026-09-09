from datetime import datetime, timezone


def create_ecg_record(device_id, ecg_voltage):
    """
    Creates an ECG data record with auto-generated timestamp.
    Timestamp is created at the moment this function is called (real-time).

    Args:
        device_id (str): Device identifier (e.g., "driver_001")
        ecg_voltage (float): ECG voltage reading from AD8232 (in volts)

    Returns:
        dict: Dictionary with keys: timestamp, device_id, ecg_voltage
    """
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "device_id": device_id,
        "ecg_voltage": ecg_voltage
    }


def create_ppg_record(device_id, ppg_ir, ppg_red):
    """
    Creates a PPG data record with auto-generated timestamp.
    Timestamp is created at the moment this function is called (real-time).

    Args:
        device_id (str): Device identifier (e.g., "driver_001")
        ppg_ir (int): Infrared light intensity from MAX30102 (0-65535)
        ppg_red (int): Red light intensity from MAX30102 (0-65535)

    Returns:
        dict: Dictionary with keys: timestamp, device_id, ppg_ir, ppg_red
    """
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "device_id": device_id,
        "ppg_ir": ppg_ir,
        "ppg_red": ppg_red
    }


def create_mpu6050_record(device_id, acceleration_x, acceleration_y, acceleration_z):
    """
    Creates an MPU6050 motion data record with auto-generated timestamp.
    Timestamp is created at the moment this function is called (real-time).

    Args:
        device_id (str): Device identifier (e.g., "driver_001")
        acceleration_x (float): X-axis acceleration from MPU6050 (in g)
        acceleration_y (float): Y-axis acceleration from MPU6050 (in g)
        acceleration_z (float): Z-axis acceleration from MPU6050 (in g)

    Returns:
        dict: Dictionary with keys: timestamp, device_id, acceleration_x, acceleration_y, acceleration_z
    """
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "device_id": device_id,
        "acceleration_x": acceleration_x,
        "acceleration_y": acceleration_y,
        "acceleration_z": acceleration_z
    }


def create_temperature_record(device_id, temperature_c):
    """
    Creates a temperature data record with auto-generated timestamp.
    Timestamp is created at the moment this function is called (real-time).

    Args:
        device_id (str): Device identifier (e.g., "driver_001")
        temperature_c (float): Temperature reading from GY-906 (in Celsius)

    Returns:
        dict: Dictionary with keys: timestamp, device_id, temperature_c
    """
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "device_id": device_id,
        "temperature_c": temperature_c
    }
