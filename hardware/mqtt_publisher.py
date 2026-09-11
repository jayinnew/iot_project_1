import paho.mqtt.client as mqtt
import json
import sys
import os

# Add parent directory to path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hardware.constants import (
    MQTT_BROKER_HOST,
    MQTT_BROKER_PORT
)


def publish_sensor_data(topic, data):
    """
    Publishes sensor data to MQTT broker in JSON format.
    Used for testing the pipeline with simulated sensor data.

    Args:
        topic (str): MQTT topic to publish to
                     Example: "sensors/driver_001/ecg"
        data (dict): Sensor data dictionary with timestamp and values
                     Example: {"timestamp": "2026-09-10T10:00:14Z", "device_id": "driver_001", "ecg_voltage": 0.85}

    Returns:
        bool: True if successful, False if failed
    """
    try:
        # Step 1: Create MQTT client instance
        # mqtt.Client() creates a new MQTT client that we'll use to connect and publish
        client = mqtt.Client()

        # Step 2: Connect to MQTT broker
        # client.connect() establishes a connection to the broker
        # MQTT_BROKER_HOST = "localhost" (defined in constants.py)
        # MQTT_BROKER_PORT = 1883 (defined in constants.py, standard MQTT port)
        # keepalive=60 means the broker will check connection every 60 seconds
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, keepalive=60)

        # Step 3: Convert sensor data dictionary to JSON string
        # json.dumps() converts the Python dict to a JSON string
        # Example: {"timestamp": "...", "device_id": "driver_001", "ecg_voltage": 0.85}
        payload = json.dumps(data)

        # Step 4: Publish the JSON payload to the MQTT topic
        # client.publish(topic, payload) sends the message to the broker
        # The broker will route it to all subscribers listening on that topic
        # Example topic: "sensors/driver_001/ecg"
        client.publish(topic, payload)

        # Step 5: Print success message
        print(f"✓ Published to {topic}: {data}")

        # Step 6: Disconnect from broker
        # client.disconnect() closes the connection gracefully
        # This frees up the connection so other clients can use it
        client.disconnect()

        # Step 7: Return True to indicate success
        return True

    except Exception as e:
        # If anything goes wrong, print error and return False
        print(f"✗ Failed to publish to {topic}: {e}")
        return False
