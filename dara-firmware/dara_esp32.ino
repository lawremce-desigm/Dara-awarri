#include <WiFi.h>
#include <WebServer.h>

// ---------------------------------------------------
// WIFI CONFIGURATION
// REPLACE WITH YOUR NETWORK CREDENTIALS
// ---------------------------------------------------
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// ---------------------------------------------------
// PIN DEFINITIONS
// ---------------------------------------------------
// On most ESP32 Dev Boards, GPIO 2 is the built-in LED.
const int LIGHT_PIN = 2; 
const int FAN_PIN = 5;

// Create WebServer object on port 80
WebServer server(80);

// ---------------------------------------------------
// SETUP
// ---------------------------------------------------
void setup() {
  Serial.begin(115200);

  // Initialize Pins
  pinMode(LIGHT_PIN, OUTPUT);
  pinMode(FAN_PIN, OUTPUT);
  
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
  
  // 1. Light Control
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

  // 2. Fan Control
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

  // 3. Temperature Check
  server.on("/temperature", HTTP_GET, []() {
    // SIMULATED SENSOR READING
    // To use a real DHT11/DHT22:
    // 1. Install "DHT sensor library" by Adafruit
    // 2. #include "DHT.h"
    // 3. dht.readTemperature();
    
    float simulatedTemp = 24.5 + (random(0, 20) / 10.0); // 24.5 - 26.5
    String tempStr = String(simulatedTemp, 1) + " °C";
    
    server.send(200, "text/plain", tempStr);
    Serial.println("Command: Check Temperature -> " + tempStr);
  });

  // 4. Health Check
  server.on("/", HTTP_GET, []() {
    server.send(200, "text/plain", "Dara ESP32 Controller is Online");
  });

  /* 
   * BLUETOOTH NOTE:
   * To implement Bluetooth Low Energy (BLE) control:
   * 1. Include <BLEDevice.h>, <BLEServer.h>, <BLEUtils.h>, <BLE2902.h>
   * 2. Create BLE Service and Characteristics for Light/Fan
   * 3. This requires significant changes to the Flutter App (using flutter_blue_plus)
   * 4. For now, we are sticking to WiFi for consistency with existing app architecture.
   */

  // Start Server
  server.begin();
  Serial.println("HTTP server started");
}

// ---------------------------------------------------
// LOOP
// ---------------------------------------------------
void loop() {
  server.handleClient();
}
