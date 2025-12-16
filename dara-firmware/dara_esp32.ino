#include <WiFi.h>
#include <WebServer.h>

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
    // For now, just simulating a sensor reading.
    // If I add a real DHT11 later, I'll need the Adafruit library here.
    float simulatedTemp = 24.5 + (random(0, 20) / 10.0); // 24.5 - 26.5
    String tempStr = String(simulatedTemp, 1) + " °C";
    
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
