# IoT Driver Monitoring System

## Data Flow

1. ESP32 reads four sensors: ECG, PPG, Motion, and Temperature
2. Sensor data publishes to MQTT broker running on localhost port 1883
3. Four separate Python subscribers listen to different sensor topics
4. Each subscriber receives data and validates the values
5. Valid data gets stored in PostgreSQL database tables

## Technologies Used

1. ESP32 microcontroller with four sensor modules
2. Mosquitto MQTT broker for message routing
3. Python with paho-mqtt library for MQTT communication
4. PostgreSQL database for storing sensor readings
5. JSON format for data transmission

## Quick Start

Start Mosquitto broker, run the four subscribers in separate terminals, then run the test pipeline to see data flow end-to-end into the database.
