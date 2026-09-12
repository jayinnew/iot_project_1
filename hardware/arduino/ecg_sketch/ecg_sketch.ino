// ECG Sensor Sketch - AD8232 for ESP32
// Reads ECG data from analog pin and publishes to MQTT

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ===== USER CONFIG - CHANGE THESE =====
const char* ssid = "OPPO F31 5G k3r6";        // Your phone's hotspot name
const char* password = "gfduvd6drcuhd67g5y7ig6gi"; // Your hotspot password
const char* mqtt_server = "10.227.254.31";      // Your laptop IP (from hostname -I)
const int mqtt_port = 1883;
// ========================================

// Device & Topic Config
const char* device_id = "driver_001";
const char* mqtt_topic = "sensors/driver_001/ecg";
const char* mqtt_client_id = "esp32_ecg_001";
const int sample_rate_ms = 100;

// Pin Config (ESP32 ADC pins: 32, 33, 34, 35, 36, 39)
const int ECG_PIN = 34;  // AD8232 OUT -> GPIO34 (ADC1_CH6)

// ADC Config (ESP32: 12-bit ADC = 0-4095, 3.3V reference)
const float adc_ref_voltage = 3.3;
const int adc_max_value = 4095;

// Global objects
WiFiClient espClient;
PubSubClient client(espClient);

unsigned long last_sample_time = 0;

void setup() {
  Serial.begin(115200);
  delay(500);

  Serial.println("\n\n=== ECG Sensor Sketch (ESP32) ===");
  Serial.print("ECG Pin: GPIO");
  Serial.println(ECG_PIN);
  Serial.print("ADC Reference: ");
  Serial.print(adc_ref_voltage);
  Serial.println("V");
  Serial.print("Sample Rate: ");
  Serial.print(sample_rate_ms);
  Serial.println("ms");

  // ADC attenuation for full 3.3V range
  analogReadResolution(12);  // 12-bit (0-4095)
  analogSetAttenuation(ADC_11db);  // 3.3V full scale

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
    readAndPublishECG();
  }
}

void readAndPublishECG() {
  // Read raw ADC
  int raw_value = analogRead(ECG_PIN);

  // Convert to voltage (0-3.3V)
  float voltage = (raw_value / (float)adc_max_value) * adc_ref_voltage;

  // Normalize to -1.0 to +1.0 range (center at 1.65V for bipolar signal)
  // AD8232 outputs ~1.65V at rest, swings ±1.65V
  float ecg_voltage = (voltage - (adc_ref_voltage / 2.0)) / (adc_ref_voltage / 2.0);

  // Clamp to validation range
  if (ecg_voltage > 1.0) ecg_voltage = 1.0;
  if (ecg_voltage < -1.0) ecg_voltage = -1.0;

  // Create JSON payload with ISO 8601 timestamp
  // Skip publish until NTP time is synced (timestamp would be invalid for DB)
  String iso_time = getISOTime();
  if (iso_time.length() == 0) {
    Serial.println("Skipping publish: waiting for NTP time sync...");
    return;
  }

  StaticJsonDocument<256> doc;
  doc["timestamp"] = iso_time;
  doc["device_id"] = device_id;
  doc["ecg_voltage"] = ecg_voltage;

  char buffer[256];
  serializeJson(doc, buffer);

  if (client.publish(mqtt_topic, buffer)) {
    Serial.print("Published ECG: ");
    Serial.println(buffer);
  } else {
    Serial.println("Failed to publish ECG");
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
  if (!getLocalTime(&timeinfo) || timeinfo.tm_year < 120) {  // year < 2020 = no NTP sync yet
    return "";
  }

  char buffer[32];
  strftime(buffer, sizeof(buffer), "%Y-%m-%dT%H:%M:%S", &timeinfo);
  // Add milliseconds
  unsigned long ms = millis() % 1000;
  String iso = String(buffer) + "." + String(ms) + "Z";
  return iso;
}
