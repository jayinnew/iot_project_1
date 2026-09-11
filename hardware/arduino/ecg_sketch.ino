// ECG Sensor Sketch - AD8232
// Reads ECG data from analog pin and publishes to MQTT

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// WiFi Configuration
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// MQTT Configuration
const char* mqtt_server = "192.168.1.100";  // Change to your laptop IP
const int mqtt_port = 1883;
const char* mqtt_client_id = "ecg_sensor_001";

// Pin Configuration (Works with any Arduino board)
const int ECG_PIN = A0;  // Analog pin for ECG sensor (AD8232)

// Device Configuration
const char* device_id = "driver_001";
const char* mqtt_topic = "sensors/driver_001/ecg";
const int sample_rate_ms = 100;

// ADC Configuration
const float adc_ref_voltage = 5.0;  // Arduino reference voltage
const int adc_max_value = 1023;     // 10-bit ADC

// Global objects
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  delay(100);

  Serial.println("\n\nECG Sensor Sketch Starting...");
  Serial.print("ECG Pin: ");
  Serial.println(ECG_PIN);

  // Connect to WiFi
  connectToWiFi();

  // Setup MQTT
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  // Maintain WiFi connection
  if (WiFi.status() != WL_CONNECTED) {
    connectToWiFi();
  }

  // Maintain MQTT connection
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();

  // Read ECG sensor
  int raw_value = analogRead(ECG_PIN);

  // Convert raw ADC to voltage
  float ecg_voltage = (raw_value / (float)adc_max_value) * adc_ref_voltage;

  // Normalize to -1.0 to 1.0 range (center at 2.5V for bipolar signal)
  ecg_voltage = (ecg_voltage - (adc_ref_voltage / 2.0)) / (adc_ref_voltage / 2.0);

  // Create JSON payload
  StaticJsonDocument<200> doc;
  doc["timestamp"] = String(millis());
  doc["device_id"] = device_id;
  doc["ecg_voltage"] = ecg_voltage;

  // Serialize and publish
  char buffer[256];
  serializeJson(doc, buffer);

  if (client.publish(mqtt_topic, buffer)) {
    Serial.print("Published ECG: ");
    Serial.println(buffer);
  } else {
    Serial.println("Failed to publish ECG");
  }

  // Wait for next sample
  delay(sample_rate_ms);
}

void connectToWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFailed to connect to WiFi");
  }
}

void reconnectMQTT() {
  Serial.print("Attempting MQTT connection...");

  if (client.connect(mqtt_client_id)) {
    Serial.println("Connected to MQTT broker");
  } else {
    Serial.print("Failed, rc=");
    Serial.println(client.state());
    delay(5000);
  }
}
