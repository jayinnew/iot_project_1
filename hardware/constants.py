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
# ESP32 SENSOR CONFIGURATION
# Add sensor-specific values when hardware is connected in the lab
# ============================================

# TODO: ESP32 Pin Configuration
# ADC pins (safe for analog input):   GPIO 32, 33, 34, 35, 36, 39
# Clean ADC input-only pin:           GPIO34 (no internal pullup/pulldown)
# I2C pins: GPIO21 (SDA) and GPIO22 (SCL) - FIXED, do not change

# TODO: ECG Sensor (AD8232) - Analog Input
ECG_PIN = 34  # GPIO34 for AD8232 ECG sensor (ADC1_CH6, input-only pin)
# NOTE: AD8232 outputs analog signal (0-3.3V), ESP32 reads via ADC
# ESP32 ADC converts to 12-bit value (0-4095)

# TODO: Sensor I2C Addresses (in hexadecimal)
# These are fixed by the sensor hardware, same on any platform including ESP32
# MAX30102_ADDRESS = 0x57  # PPG sensor (MAX30102) I2C address
# MPU6050_ADDRESS = 0x68   # Motion sensor (MPU6050) I2C address
# GY906_ADDRESS = 0x5A     # Temperature sensor (GY-906) I2C address
# NOTE: I2C uses ESP32 pins GPIO21 (SDA) and GPIO22 (SCL) - hardwired, no config needed

# TODO: ADC Reference Voltage (for analog reading calibration)
ESP32_ADC_REF_VOLTAGE = 3.3  # ESP32 ADC reference (3.3V)
ESP32_ADC_MAX_VALUE = 4095   # 12-bit ADC max value (2^12 - 1)
# NOTE: Use these to convert raw ADC values to voltage: voltage = (raw_value / ADC_MAX) * REF_VOLTAGE

# TODO: Sensor Value Ranges (for validation - same across all platforms)
ECG_VOLTAGE_MIN = -1.0  # Minimum valid ECG voltage (in volts)
ECG_VOLTAGE_MAX = 1.0   # Maximum valid ECG voltage (in volts)

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
# HELPFUL REFERENCE: ESP32 PIN LAYOUT (DevKit)
# ============================================
# I2C (Fixed):          GPIO21 (SDA), GPIO22 (SCL)
# Serial (Fixed):       GPIO1 (TX), GPIO3 (RX)
# ADC (Analog in):      GPIO32, 33, 34, 35, 36, 39
# Strapping pins (AVOID): GPIO0, GPIO2, GPIO12, GPIO15
#
# Available for sensors:
# - I2C sensors: PPG (MAX30102), Motion (MPU6050), Temp (MLX90614)
#   all share the same bus: GPIO21/GPIO22
# - ECG analog: GPIO34 (input-only, clean ADC channel)
# - Power: all sensors at 3.3V (ESP32 is 3.3V logic, NOT 5V tolerant!)
