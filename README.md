# Dára Home (Dara-awarri)

**Dára Home** is a multilingual, voice-first smart home assistant designed specifically for the Nigerian context. It bridges the gap between modern smart home technology and local linguistic reality by supporting **English, Yoruba, Hausa, and Igbo**.

## 🏗️ Architecture Overview

The system operates on a **Controller-Facilitator** model where the Mobile App acts as the central brain for orchestration, while the Backend handles intelligence and the ESP32 handles physical execution.

```mermaid
flowchart LR
    User((User)) <--> App[📱 Mobile App\n(Flutter)]
    App <--> Backend[🧠 Backend API\n(FastAPI)]
    App --> ESP32[💡 Device Controller\n(ESP32 / C++)]
    
    subgraph Cloud Intelligence
        Backend --> Whisper[Speech-to-Text\n(Deepgram)]
        Backend --> ATLAS[Intent/Reasoning\n(N-ATLaS / Modal)]
        Backend --> TTS[Text-to-Speech\n(Google/Edge)]
    end

    subgraph Physical World
        ESP32 --> Light[Lights]
        ESP32 --> Fan[Fans]
        ESP32 -- GPIO 4 --> Temp[DHT11 Sensor]
    end
```

### 🔄 How It Works
1.  **Voice Command**: The user speaks into the **Mobile App** (e.g., *"Tan ina yara mi"* - Turn on my room light).
2.  **Processing**: The app sends the audio to the **Backend**.
3.  **Intelligence**:
    *   **STT**: Audio is transcribed to text (e.g., "Tan ina yara mi").
    *   **Reasoning**: The N-ATLaS model (finetuned LLM) analyzes the text, detects the language (`yo`), intent (`INSTRUCTION`), action (`TURN_ON`), and device (`LIGHT`).
    *   **Response**: The system generates a natural text response in the same language and converts it to audio.
4.  **Action**: The Backend returns the *Intent* and *Audio* to the App.
5.  **Execution**:
    *   The **App** plays the audio response to the user.
    *   If an action is required, the **App** directly calls the **ESP32** over the local network (e.g., `POST http://<ESP_IP>/light/turn/on`).

---

## 📂 Repository Structure

This monorepo contains three distinct components:

### 1. `dara-mobile-app/` (Flutter)
The user interface and central controller.
*   **Features/Roles**: Voice recording, audio playback, state management (`AppState`), and direct HTTP control of local ESP32 devices.
*   **Key Tech**: Flutter, Provider, HTTP, Audio Players.

### 2. `dara-backend/` (FastAPI / Python)
The intelligence layer hosted in the cloud/locally.
*   **Features/Roles**: Speech-to-Text (Deepgram), Intent Classification (N-ATLaS on Modal), Text-to-Speech.
*   **Key Tech**: Python, FastAPI, Modal, requests.

### 3. `dara-firmware/` (C++ / Arduino)
The code running on the ESP32 microcontroller.
*   **Features/Roles**: Connects to WiFi, listens for HTTP commands to toggle GPIO pins (Lights/Fans), and reads sensor data (DHT11).
*   **Key Tech**: C++, Arduino Framework, ESP32 WebServer, Adafruit DHT Library.

---

## 🚀 Getting Started

### Prerequisites
*   **Hardware**: ESP32 Development Board, DHT11 Sensor, LEDs/Relays.
*   **Software**: Flutter SDK, Python 3.9+, Arduino IDE.

### Setup Guide

#### 1. Firmware (ESP32)
1.  Open `dara-firmware/dara_esp32.ino` in Arduino IDE.
2.  Install the **"DHT sensor library"** by Adafruit via Library Manager.
3.  Update the specific lines for your WiFi credentials:
    ```cpp
    const char* ssid = "YOUR_WIFI_NAME";
    const char* password = "YOUR_WIFI_PASSWORD";
    ```
4.  Flash to your ESP32. Note the IP address printed in the Serial Monitor.

#### 2. Backend
1.  Navigate to `dara-backend/`.
2.  Install dependencies: `pip install -r requirements.txt`.
3.  Set up your `.env` file with API keys (Deepgram, Modal/OpenAI, etc.).
4.  Run the server: `python main.py`.

#### 3. Mobile App
1.  Navigate to `dara-mobile-app/`.
2.  Run `flutter pub get`.
3.  In the app settings (or code), configure the **Backend URL** and the **ESP32 IP Address**.
4.  Run on your device: `flutter run`.

---

## 🛠️ Technology Stack
*   **Mobile**: Flutter (Dart)
*   **Backend**: FastAPI (Python)
*   **AI/ML**:
    *   *Intent*: N-ATLaS (Nigerian Aggregated Text & Linguistic and Speech dataset) served via Modal.
    *   *STT*: Deepgram Nova-2 / OpenAI Whisper.
    *   *TTS*: Edge-TTS / Google TTS.
*   **IoT**: ESP32 (C++ / Arduino).

## 📄 License
Property of **Zamari Labs**.
