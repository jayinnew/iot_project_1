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
    Subscribes to Temperature sensor topic only.

    Args:
        client (mqtt.Client): MQTT client instance
        userdata: User data passed to callback
        flags: Connection flags
        rc (int): Connection result code (0 = success)
    """
    if rc == 0:
        print(f"✓ [TEMP] Connected to MQTT broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}")
        # Subscribe to Temperature sensor topic only
        topic = f"sensors/{DEVICE_ID}/temperature"
        client.subscribe(topic)
        print(f"✓ [TEMP] Subscribed to: {topic}")
    else:
        print(f"✗ [TEMP] Connection failed with code {rc}")


def on_disconnect(client, userdata, rc):
    """
    Callback function when MQTT client disconnects from broker.

    Args:
        client (mqtt.Client): MQTT client instance
        userdata: User data passed to callback
        rc (int): Disconnection result code
    """
    if rc != 0:
        print(f"✗ [TEMP] Unexpected disconnection from broker (code: {rc})")
    else:
        print("✓ [TEMP] Disconnected from MQTT broker")


def on_message(client, userdata, msg):
    """
    Callback function when a message arrives on Temperature topic.
    Converts JSON to Python dictionary and inserts into database.

    Args:
        client (mqtt.Client): MQTT client instance
        userdata: User data passed to callback
        msg (mqtt.MQTTMessage): The message object containing payload
    """
    try:
        # msg.payload is bytes, need to convert to string then JSON
        payload_json = msg.payload.decode('utf-8')

        # Convert JSON string to Python dictionary
        payload_dict = json.loads(payload_json)

        if LOG_SENSOR_READINGS:
            print(f"✓ [TEMP] Received: {payload_dict}")

        # Insert data into database
        insert_temperature_data(payload_dict)

    except json.JSONDecodeError as e:
        print(f"✗ [TEMP] Failed to decode JSON: {e}")
    except Exception as e:
        print(f"✗ [TEMP] Error processing message: {e}")


def insert_temperature_data(data):
    """
    Inserts Temperature data into database.
    Validates and calls database layer.

    Args:
        data (dict): Temperature sensor data dictionary
    """
    try:
        from backend.database import insert_sensor_data

        # Insert into temperature_data table
        result = insert_sensor_data('temperature_data', data)

        if not result:
            print(f"✗ [TEMP] Failed to insert data into database")

    except Exception as e:
        print(f"✗ [TEMP] Error inserting data: {e}")


def start_temperature_subscriber():
    """
    Starts the Temperature MQTT subscriber and connects to the broker.
    Runs indefinitely, listening for messages on Temperature topic.
    """
    # Create MQTT client instance
    client = mqtt.Client()

    # Set callback functions
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    try:
        print(f"[TEMP] Connecting to MQTT broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}...")
        # Connect to MQTT broker
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, keepalive=60)

        # Start the network loop (this runs forever)
        print("[TEMP] Starting subscriber loop...")
        client.loop_forever()

    except KeyboardInterrupt:
        print("\n[TEMP] Subscriber stopped by user")
    except Exception as e:
        print(f"[TEMP] Error: {e}")
    finally:
        client.disconnect()
        print("[TEMP] MQTT client stopped")


if __name__ == "__main__":
    print("=" * 50)
    print("TEMPERATURE SENSOR SUBSCRIBER")
    print("=" * 50)
    print(f"Device: {DEVICE_ID}")
    print(f"Listening for: sensors/{DEVICE_ID}/temperature")
    print("=" * 50)
    start_temperature_subscriber()
