import time
import sys
import os

# Add parent directory to path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from hardware.sensor_reader import read_all_sensors
from hardware.mqtt_publisher import publish_sensor_data
from hardware.constants import DEVICE_ID, SAMPLE_RATE_MS


def test_pipeline():
    """
    Main testing function that simulates Arduino behavior.
    Reads simulated sensor data and publishes to MQTT broker.
    This tests the complete pipeline end-to-end before connecting real Arduino.

    Process:
    1. Read all 4 sensors using sensor_reader.py (simulated data)
    2. Publish each sensor's data to MQTT using mqtt_publisher.py
    3. 4 separate subscribers receive the data
    4. Subscribers validate and insert into PostgreSQL
    5. Repeat every 100ms (SAMPLE_RATE_MS)
    """

    print("=" * 60)
    print("IOT DRIVER MONITORING - TEST PIPELINE")
    print("=" * 60)
    print(f"Device: {DEVICE_ID}")
    print(f"Sampling Rate: {SAMPLE_RATE_MS}ms")
    print(f"MQTT Topics:")
    print(f"  - sensors/{DEVICE_ID}/ecg")
    print(f"  - sensors/{DEVICE_ID}/ppg")
    print(f"  - sensors/{DEVICE_ID}/mpu6050")
    print(f"  - sensors/{DEVICE_ID}/temperature")
    print("=" * 60)
    print("Starting test loop. Press Ctrl+C to stop.\n")

    try:
        # Infinite loop - continues until user presses Ctrl+C
        while True:
            # Step 1: Read all sensors at once
            # read_all_sensors() returns a dictionary with keys: 'ecg', 'ppg', 'mpu6050', 'temperature'
            # Each value is a record dict with: timestamp, device_id, and sensor-specific values
            all_sensor_data = read_all_sensors(DEVICE_ID)

            # Step 2: Publish ECG data
            # Topic: sensors/driver_001/ecg
            # Data: {timestamp, device_id, ecg_voltage}
            publish_sensor_data(
                f"sensors/{DEVICE_ID}/ecg",
                all_sensor_data['ecg']
            )

            # Step 3: Publish PPG data
            # Topic: sensors/driver_001/ppg
            # Data: {timestamp, device_id, ppg_ir, ppg_red}
            publish_sensor_data(
                f"sensors/{DEVICE_ID}/ppg",
                all_sensor_data['ppg']
            )

            # Step 4: Publish MPU6050 data
            # Topic: sensors/driver_001/mpu6050
            # Data: {timestamp, device_id, acceleration_x, acceleration_y, acceleration_z}
            publish_sensor_data(
                f"sensors/{DEVICE_ID}/mpu6050",
                all_sensor_data['mpu6050']
            )

            # Step 5: Publish Temperature data
            # Topic: sensors/driver_001/temperature
            # Data: {timestamp, device_id, temperature_c}
            publish_sensor_data(
                f"sensors/{DEVICE_ID}/temperature",
                all_sensor_data['temperature']
            )

            # Step 6: Sleep for SAMPLE_RATE_MS before reading sensors again
            # SAMPLE_RATE_MS = 100 (defined in constants.py)
            # This means: read and publish all sensors every 100ms (10 times per second)
            time.sleep(SAMPLE_RATE_MS / 1000)  # Convert milliseconds to seconds

    except KeyboardInterrupt:
        # User pressed Ctrl+C
        print("\n" + "=" * 60)
        print("Test pipeline stopped by user")
        print("=" * 60)
        return True

    except Exception as e:
        # If any error occurs, print it and return False
        print(f"\n✗ Error in test pipeline: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # This runs when you execute: python test_pipeline.py
    success = test_pipeline()
    sys.exit(0 if success else 1)
