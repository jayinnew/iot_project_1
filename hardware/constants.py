# ============================================
# HARDWARE CONSTANTS
# ============================================
# Configuration values for sensors and devices
# Add sensor-specific values when hardware is connected

# Device Identification
DEVICE_ID = "driver_001"
# Unique identifier for this hardware device
# Used to track which device sent sensor data

# Sampling Configuration
SAMPLE_RATE_MS = 100
# Sampling interval in milliseconds (100ms = 10 samples per second)
# How often sensors are read and data is sent to backend

# MQTT Broker Configuration
MQTT_BROKER_HOST = "localhost"
# IP address or hostname where MQTT broker is running
# Change to your broker IP if running on different machine
# For Docker/remote: change to server IP address

MQTT_BROKER_PORT = 1883
# Port number where MQTT broker is listening
# Standard MQTT port is 1883 (unencrypted)
# Use 8883 for encrypted MQTT (TLS)

# MQTT Topics (publish sensor data to these topics)
MQTT_TOPIC_ECG = "sensors/driver_001/ecg"
# Topic for ECG (AD8232) sensor data
# Hardware publishes to this topic

MQTT_TOPIC_PPG = "sensors/driver_001/ppg"
# Topic for PPG (MAX30102) sensor data
# Hardware publishes to this topic

MQTT_TOPIC_MPU6050 = "sensors/driver_001/mpu6050"
# Topic for MPU6050 motion sensor data
# Hardware publishes to this topic

MQTT_TOPIC_TEMPERATURE = "sensors/driver_001/temperature"
# Topic for temperature (GY-906) sensor data
# Hardware publishes to this topic

# Retry Configuration
MAX_RETRIES = 3
# Maximum number of times to retry sending data if connection fails

RETRY_DELAY_MS = 1000
# Delay in milliseconds between retry attempts

# Logging Configuration
LOG_SENSOR_READINGS = True
# Whether to print sensor readings to console (useful for debugging)

LOG_FAILED_SENDS = True
# Whether to log failed data transmission attempts


# ============================================
# SENSOR CONFIGURATION - ADD WHEN SENSORS ARE CONNECTED
# ============================================

# TODO: I2C Configuration (for Raspberry Pi sensors)
# I2C_BUS = 1  # I2C bus number on Raspberry Pi (typically 1)

# TODO: Sensor I2C Addresses (in hexadecimal)
# MAX30102_ADDRESS = 0x57  # PPG sensor (MAX30102) I2C address
# MPU6050_ADDRESS = 0x68   # Motion sensor (MPU6050) I2C address
# GY906_ADDRESS = 0x5A     # Temperature sensor (GY-906) I2C address

# TODO: ECG Sensor (AD8232) Configuration
# ECG_PIN = 17  # GPIO pin number on Raspberry Pi for AD8232 ECG sensor
# NOTE: AD8232 outputs analog signal, requires ADC (Analog-to-Digital Converter)

# TODO: Sensor Value Ranges (for validation)
# ECG_VOLTAGE_MIN = -1.0  # Minimum valid ECG voltage (in volts)
# ECG_VOLTAGE_MAX = 1.0   # Maximum valid ECG voltage (in volts)

# PPG_IR_MIN = 0      # Minimum valid PPG infrared intensity
# PPG_IR_MAX = 65535  # Maximum valid PPG infrared intensity (16-bit unsigned)

# PPG_RED_MIN = 0     # Minimum valid PPG red light intensity
# PPG_RED_MAX = 65535 # Maximum valid PPG red light intensity (16-bit unsigned)

# ACCELERATION_MIN = -16.0  # Minimum valid acceleration (in g)
# ACCELERATION_MAX = 16.0   # Maximum valid acceleration (in g)
# NOTE: MPU6050 typically outputs ±16g range

# TEMPERATURE_MIN = 20.0  # Minimum valid body temperature (in Celsius)
# TEMPERATURE_MAX = 45.0  # Maximum valid body temperature (in Celsius)
# NOTE: Normal human body temperature is 36-37°C, range allows for sensor tolerance
