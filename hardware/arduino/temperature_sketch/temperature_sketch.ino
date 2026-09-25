// Temperature Sensor Sketch - MLX90614 (GY-906) for ESP32
// Reads object temperature via I2C and publishes to MQTT

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_MLX90614.h>  // Adafruit MLX90614 library

// ===== USER CONFIG - CHANGE THESE =====
const char* ssid = "OPPO F31 5G k3r6";            // Your phone's hotspot name
const char* password = "gfduvd6drcuhd67g5y7ig6gi"; // Your hotspot password
const char* mqtt_server = "10.224.23.31";           // Your laptop IP (from hostname -I)
const int mqtt_port = 1883;
// ========================================

// Device & Topic Config
const char* device_id = "driver_001";
const char* mqtt_topic = "sensors/driver_001/temperature";
const char* mqtt_client_id = "esp32_temperature_001";
const int sample_rate_ms = 100;  // 100ms = 10 samples/sec (matches backend)

// I2C pins (ESP32 defaults: SDA=GPIO21, SCL=GPIO22)
// MLX90614 I2C address: 0x5A (fixed by hardware)

// Global objects
WiFiClient espClient;
PubSubClient client(espClient);
Adafruit_MLX90614 mlx;

unsigned long last_sample_time = 0;

void setup() {
  Serial.begin(115200);
  delay(500);

  Serial.println("\n\n=== Temperature Sensor Sketch (ESP32) ===");
  Serial.println("Sensor: MLX90614 (GY-906)");
  Serial.println("I2C: SDA=GPIO21, SCL=GPIO22, addr=0x5A");
  Serial.print("Sample Rate: ");
  Serial.print(sample_rate_ms);
  Serial.println("ms");

  // Initialize I2C with ESP32 default pins
  Wire.begin(21, 22);  // SDA=GPIO21, SCL=GPIO22

  // Initialize MLX90614
  if (!mlx.begin()) {
    Serial.println("ERROR: MLX90614 not found. Check wiring:");
    Serial.println("  VCC  -> 3.3V");
    Serial.println("  GND  -> GND");
    Serial.println("  SDA  -> GPIO21");
    Serial.println("  SCL  -> GPIO22");
    Serial.println("NOTE: MLX90614 needs 10k pull-up resistors on SDA and SCL");
    while (true) delay(1000);
  }

  Serial.println("MLX90614 initialized OK");

  connectToWiFi();

  // Sync real time via NTP so timestamps are valid PostgreSQL TIMESTAMPTZ
  configTime(0, 0, "pool.ntp.org", "time.nist.gov");

  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  // WiFi auto-reconnects in the background (ESP32 default) - do NOT call
  // WiFi.begin() again here; it errors with "wifi:sta is connecting, cannot set config".

  if (WiFi.status() != WL_CONNECTED) {
    // WiFi down: report once every 10s, skip MQTT/sensor until connected
    static unsigned long last_report = 0;
    if (millis() - last_report > 10000) {
      last_report = millis();
      Serial.println("WiFi not connected - auto-reconnecting in background...");
    }
    return;  // wait for WiFi before doing anything
  }

  // Maintain MQTT
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();

  // Read sensor at sample rate
  unsigned long now = millis();
  if (now - last_sample_time >= sample_rate_ms) {
    last_sample_time = now;
    readAndPublishTemperature();
  }
}

void readAndPublishTemperature() {
  // Read object temperature in Celsius
  // getObjectTempC() returns the temperature of the object the sensor points at
  float temp_c = mlx.getObjectTempC();

  // Validate reading: NaN or clearly out-of-range means sensor error
  if (isnan(temp_c) || temp_c < -40.0 || temp_c > 125.0) {
    Serial.print("WARNING: bogus temperature reading: ");
    Serial.println(temp_c);
    return;  // skip this sample completely
  }

  // Clamp to DB validation range (20–45°C)
  // Values outside this range are rejected by backend/database.py
  if (temp_c < 20.0) temp_c = 20.0;
  if (temp_c > 45.0) temp_c = 45.0;

  // Skip publish until NTP time is synced (timestamp would be invalid for DB)
  String iso_time = getISOTime();
  if (iso_time.length() == 0) {
    Serial.println("Skipping publish: waiting for NTP time sync...");
    return;
  }

  // Build JSON payload matching backend validation:
  //   temperature_c -> FLOAT, 20.0–45.0 °C
  StaticJsonDocument<256> doc;
  doc["timestamp"]     = iso_time;
  doc["device_id"]     = device_id;
  doc["temperature_c"] = temp_c;

  char buffer[256];
  serializeJson(doc, buffer);

  if (client.publish(mqtt_topic, buffer)) {
    Serial.print("Published TEMP: ");
    Serial.println(buffer);
  } else {
    Serial.println("Failed to publish TEMP");
  }
}

void connectToWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
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
    Serial.println("Connected!");
  } else {
    Serial.print("Failed, rc=");
    Serial.print(client.state());
    Serial.println(" Retrying in 5s...");
    delay(5000);
  }
}

// Generate ISO 8601 timestamp (matches backend format).
// Returns empty string if NTP time is not synced yet,
// so invalid timestamps are never sent to the database.
String getISOTime() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo) || timeinfo.tm_year < 120) {  // year < 2020 = not synced
    return "";
  }

  char buffer[32];
  strftime(buffer, sizeof(buffer), "%Y-%m-%dT%H:%M:%S", &timeinfo);
  // Add milliseconds
  unsigned long ms = millis() % 1000;
  String iso = String(buffer) + "." + String(ms) + "Z";
  return iso;
}
