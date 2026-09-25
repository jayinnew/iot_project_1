// MPU6050 Motion Sensor Sketch for ESP32
// Reads 3-axis acceleration via I2C and publishes to MQTT

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <MPU6050_light.h>  // MPU6050_light library by rfetick

// ===== USER CONFIG - CHANGE THESE =====
const char* ssid = "OPPO F31 5G k3r6";            // Your phone's hotspot name
const char* password = "gfduvd6drcuhd67g5y7ig6gi"; // Your hotspot password
const char* mqtt_server = "10.224.23.31";           // Your laptop IP (from hostname -I)
const int mqtt_port = 1883;
// ========================================

// Device & Topic Config
const char* device_id = "driver_001";
const char* mqtt_topic = "sensors/driver_001/mpu6050";
const char* mqtt_client_id = "esp32_mpu6050_001";
const int sample_rate_ms = 100;  // 100ms = 10 samples/sec (matches backend)

// I2C pins (ESP32 defaults: SDA=GPIO21, SCL=GPIO22)
// MPU6050 I2C address: 0x68 (AD0 pin LOW, the default)

// Global objects
WiFiClient espClient;
PubSubClient client(espClient);
MPU6050 mpu(Wire);

unsigned long last_sample_time = 0;

void setup() {
  Serial.begin(115200);
  delay(500);

  Serial.println("\n\n=== MPU6050 Motion Sensor Sketch (ESP32) ===");
  Serial.println("Sensor: MPU6050");
  Serial.println("I2C: SDA=GPIO21, SCL=GPIO22, addr=0x68");
  Serial.print("Sample Rate: ");
  Serial.print(sample_rate_ms);
  Serial.println("ms");

  // Initialize I2C with ESP32 default pins
  Wire.begin(21, 22);  // SDA=GPIO21, SCL=GPIO22

  // Initialize MPU6050
  byte status = mpu.begin();
  if (status != 0) {
    Serial.print("ERROR: MPU6050 init failed, code=");
    Serial.println(status);
    Serial.println("Check wiring:");
    Serial.println("  VCC  -> 3.3V");
    Serial.println("  GND  -> GND");
    Serial.println("  SDA  -> GPIO21");
    Serial.println("  SCL  -> GPIO22");
    Serial.println("  AD0  -> GND  (sets I2C addr to 0x68)");
    while (true) delay(1000);
  }

  Serial.println("Calibrating MPU6050 (keep still for 3s)...");
  delay(1000);
  mpu.calcOffsets(true, true);  // calculates gyro and accel offsets
  Serial.println("MPU6050 initialized and calibrated OK");

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

  // Update MPU6050 internal registers (must be called regularly)
  mpu.update();

  // Read sensor at sample rate
  unsigned long now = millis();
  if (now - last_sample_time >= sample_rate_ms) {
    last_sample_time = now;
    readAndPublishMPU6050();
  }
}

void readAndPublishMPU6050() {
  // Read acceleration in g (gravity units, ±16g range)
  float accel_x = mpu.getAccX();
  float accel_y = mpu.getAccY();
  float accel_z = mpu.getAccZ();

  // Clamp to DB validation range (±16g)
  auto clamp = [](float v, float lo, float hi) {
    return v < lo ? lo : (v > hi ? hi : v);
  };
  accel_x = clamp(accel_x, -16.0f, 16.0f);
  accel_y = clamp(accel_y, -16.0f, 16.0f);
  accel_z = clamp(accel_z, -16.0f, 16.0f);

  // Skip publish until NTP time is synced (timestamp would be invalid for DB)
  String iso_time = getISOTime();
  if (iso_time.length() == 0) {
    Serial.println("Skipping publish: waiting for NTP time sync...");
    return;
  }

  // Build JSON payload matching backend validation:
  //   acceleration_x/y/z -> FLOAT, ±16g
  StaticJsonDocument<256> doc;
  doc["timestamp"]      = iso_time;
  doc["device_id"]      = device_id;
  doc["acceleration_x"] = accel_x;
  doc["acceleration_y"] = accel_y;
  doc["acceleration_z"] = accel_z;

  char buffer[256];
  serializeJson(doc, buffer);

  if (client.publish(mqtt_topic, buffer)) {
    Serial.print("Published MPU6050: ");
    Serial.println(buffer);
  } else {
    Serial.println("Failed to publish MPU6050");
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
