#include <WiFi.h>
#include <WebServer.h>
#include <DHT.h>

// ---------------------------------------------------
// ---------------------------------------------------
// NETWORK CONFIGURATION
// Wireless credentials
// ---------------------------------------------------
const char* ssid = "WIFI_SSID";
const char* password = "WIFI_PASSWORD";

// ---------------------------------------------------
// PIN DEFINITIONS
// ---------------------------------------------------
// GPIO 4 for Data, using a DHT11 sensor (blue one).
// If I ever switch to the white DHT22, I need to change DHTTYPE.
#define DHTPIN 4     
#define DHTTYPE DHT11

// Initialize DHT sensor
DHT dht(DHTPIN, DHTTYPE);

// GPIO 2 is usually the built-in LED on these boards
const int LIGHT_PIN = 2; 
const int FAN_PIN = 5;

// Create WebServer object on port 80
WebServer server(80);

// ---------------------------------------------------
// ---------------------------------------------------
// INITIALIZATION
// ---------------------------------------------------
void setup() {
  Serial.begin(115200);

  // Initialize Pins
  pinMode(LIGHT_PIN, OUTPUT);
  pinMode(FAN_PIN, OUTPUT);
  
  // Start the sensor
  dht.begin();
  
  // Default state: OFF
  digitalWrite(LIGHT_PIN, LOW);
  digitalWrite(FAN_PIN, LOW);

  // Connect to Wi-Fi
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Define HTTP Routes
  
  // Light Control
  server.on("/light/turn/on", HTTP_POST, []() {
    digitalWrite(LIGHT_PIN, HIGH);
    server.send(200, "text/plain", "Light turned ON");
    Serial.println("Command: Light ON");
  });

  server.on("/light/turn/off", HTTP_POST, []() {
    digitalWrite(LIGHT_PIN, LOW);
    server.send(200, "text/plain", "Light turned OFF");
    Serial.println("Command: Light OFF");
  });

  // Fan Control
  server.on("/fan/turn/on", HTTP_POST, []() {
    digitalWrite(FAN_PIN, HIGH);
    server.send(200, "text/plain", "Fan turned ON");
    Serial.println("Command: Fan ON");
  });

  server.on("/fan/turn/off", HTTP_POST, []() {
    digitalWrite(FAN_PIN, LOW);
    server.send(200, "text/plain", "Fan turned OFF");
    Serial.println("Command: Fan OFF");
  });

  // Temperature Check
  server.on("/temperature", HTTP_GET, []() {
    // Reading temperature or humidity takes about 250 milliseconds!
    float t = dht.readTemperature();

    // Check if any reads failed and exit early (to try again).
    if (isnan(t)) {
      Serial.println("Failed to read from DHT sensor!");
      server.send(500, "text/plain", "Sensor Error");
      return;
    }
    
    String tempStr = String(t, 1) + " °C";
    
    server.send(200, "text/plain", tempStr);
    Serial.println("Command: Check Temperature -> " + tempStr);
  });

  // Health Check
  server.on("/", HTTP_GET, []() {
    server.send(200, "text/plain", "Dara ESP32 Controller is Online");
  });

  /* 
   * FUTURE UPGRADE:
   * Bluetooth (BLE) support could be added here using <BLEDevice.h>.
   * Would need to update the Flutter app to handle the BLE handshake.
   * Keeping it simple with WiFi for now.
   */

  // Start Server
  server.begin();
  Serial.println("HTTP server started");
}

// ---------------------------------------------------
// MAIN LOOP
// ---------------------------------------------------
void loop() {
  server.handleClient();
}
