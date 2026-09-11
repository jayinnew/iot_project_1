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
# ARDUINO UNO SENSOR CONFIGURATION
# Add sensor-specific values when hardware is connected in the lab
# ============================================

# TODO: Arduino Pin Configuration (for Arduino Uno)
# Analog pins: A0-A5 (map to digital pins 14-19)
# Digital pins: 0-13
# I2C pins: A4 (SDA) and A5 (SCL) - FIXED, do not change

# TODO: ECG Sensor (AD8232) - Analog Input
# ECG_PIN = A0  # Analog pin A0 for AD8232 ECG sensor
# NOTE: AD8232 outputs analog signal (0-5V), Arduino reads via ADC on analog pins
# Arduino ADC converts to 10-bit value (0-1023)

# TODO: Sensor I2C Addresses (in hexadecimal)
# These are fixed by the sensor hardware, same on any platform including Arduino
# MAX30102_ADDRESS = 0x57  # PPG sensor (MAX30102) I2C address
# MPU6050_ADDRESS = 0x68   # Motion sensor (MPU6050) I2C address
# GY906_ADDRESS = 0x5A     # Temperature sensor (GY-906) I2C address
# NOTE: I2C uses Arduino pins A4 (SDA) and A5 (SCL) - hardwired, no config needed

# TODO: ADC Reference Voltage (for analog reading calibration)
# ARDUINO_ADC_REF_VOLTAGE = 5.0  # Arduino Uno ADC reference (5V)
# ARDUINO_ADC_MAX_VALUE = 1023   # 10-bit ADC max value (2^10 - 1)
# NOTE: Use these to convert raw ADC values to voltage: voltage = (raw_value / ADC_MAX) * REF_VOLTAGE

# TODO: Sensor Value Ranges (for validation - same across all platforms)
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

# ============================================
# HELPFUL REFERENCE: ARDUINO UNO PIN LAYOUT
# ============================================
# Analog Pins (0-5):     A0, A1, A2, A3, A4, A5
# Maps to Digital Pins:  14,  15,  16,  17,  18,  19
#
# I2C (Fixed):           A4 (SDA), A5 (SCL)
# Serial (Fixed):        0 (RX), 1 (TX)
#
# Available for sensors:
# - Analog: A0, A1, A2, A3 (A4, A5 reserved for I2C)
# - Digital: 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 (0, 1 reserved for Serial)
