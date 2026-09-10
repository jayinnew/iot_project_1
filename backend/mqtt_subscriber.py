import paho.mqtt.client as mqtt
import json
import sys
import os

# Add parent directory to path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hardware.constants import (
    DEVICE_ID,
    MQTT_BROKER_HOST,
    MQTT_BROKER_PORT,
    LOG_SENSOR_READINGS
)


def on_connect(client, userdata, flags, rc):
    """
    Callback function when MQTT client connects to broker.
    Subscribes to all sensor topics using wildcard.

    Args:
        client (mqtt.Client): MQTT client instance
        userdata: User data passed to callback
        flags: Connection flags
        rc (int): Connection result code (0 = success)
    """
    if rc == 0:
        print(f"✓ Connected to MQTT broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}")
        # Subscribe to all sensor topics for this device using wildcard
        # # = wildcard that matches everything after sensors/driver_001/
        # This subscribes to: sensors/driver_001/ecg, ppg, mpu6050, temperature
        topic_filter = f"sensors/{DEVICE_ID}/#"
        client.subscribe(topic_filter)
        print(f"✓ Subscribed to: {topic_filter}")
    else:
        print(f"✗ Connection failed with code {rc}")


def on_disconnect(client, userdata, rc):
    """
    Callback function when MQTT client disconnects from broker.

    Args:
        client (mqtt.Client): MQTT client instance
        userdata: User data passed to callback
        rc (int): Disconnection result code
    """
    if rc != 0:
        print(f"✗ Unexpected disconnection from broker (code: {rc})")
    else:
        print("✓ Disconnected from MQTT broker")


def on_message(client, userdata, msg):
    """
    Callback function when a message arrives on a subscribed topic.
    Converts JSON to Python dictionary and passes to database.py for insertion.

    Args:
        client (mqtt.Client): MQTT client instance
        userdata: User data passed to callback
        msg (mqtt.MQTTMessage): The message object containing:
                                - msg.topic: the topic string (e.g., "sensors/driver_001/ecg")
                                - msg.payload: the message bytes
    """
    try:
        # msg.payload is bytes, need to convert to string then JSON
        # Example: b'{"timestamp": "2026-09-10T10:00:14Z", "device_id": "driver_001", "ecg_voltage": 0.85}'
        payload_json = msg.payload.decode('utf-8')

        # Convert JSON string to Python dictionary
        # Example: {"timestamp": "2026-09-10T10:00:14Z", "device_id": "driver_001", "ecg_voltage": 0.85}
        payload_dict = json.loads(payload_json)

        if LOG_SENSOR_READINGS:
            print(f"✓ Received on {msg.topic}: {payload_dict}")

        # Pass dictionary to insert_data() for routing to correct database table
        insert_data(msg.topic, payload_dict)

    except json.JSONDecodeError as e:
        print(f"✗ Failed to decode JSON from topic {msg.topic}: {e}")
    except Exception as e:
        print(f"✗ Error processing message on {msg.topic}: {e}")


def insert_data(topic, data):
    """
    Routes received data to correct database table based on MQTT topic.
    Calls database.py to insert the dictionary into PostgreSQL.

    Args:
        topic (str): MQTT topic (e.g., "sensors/driver_001/ecg")
        data (dict): Sensor data dictionary with timestamp and values
                     Example: {"timestamp": "2026-09-10T10:00:14Z", "device_id": "driver_001", "ecg_voltage": 0.85}
    """
    try:
        from backend.database import insert_sensor_data

        # Extract sensor type from topic
        # Topic format: sensors/driver_001/ecg
        # We want the last part: ecg
        sensor_type = topic.split('/')[-1]

        # Map sensor type to database table name
        table_mapping = {
            'ecg': 'ecg_data',
            'ppg': 'ppg_data',
            'mpu6050': 'mpu6050_data',
            'temperature': 'temperature_data'
        }

        table_name = table_mapping.get(sensor_type)

        if table_name:
            # Call database.py to insert data
            insert_sensor_data(table_name, data)
        else:
            print(f"✗ Unknown sensor type: {sensor_type}")
    except Exception as e:
        print(f"✗ Error in insert_data: {e}")


def start_subscriber():
    """
    Starts the MQTT subscriber and connects to the broker.
    Runs indefinitely, listening for messages on subscribed topics.
    """
    # Create MQTT client instance
    client = mqtt.Client()

    # Set callback functions
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    try:
        print(f"Connecting to MQTT broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}...")
        # Connect to MQTT broker
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, keepalive=60)

        # Start the network loop (this runs forever)
        # It processes incoming messages and handles connection events
        print("Starting subscriber loop...")
        client.loop_forever()

    except KeyboardInterrupt:
        print("\nSubscriber stopped by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.disconnect()
        print("MQTT client stopped")


if __name__ == "__main__":
    print("Starting MQTT subscriber...")
    print(f"Listening for sensor data from device: {DEVICE_ID}")
    start_subscriber()
