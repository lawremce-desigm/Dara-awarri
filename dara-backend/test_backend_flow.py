import requests
import base64
import os
import json

# Configuration
API_URL = "http://127.0.0.1:8000/voice"
TEST_AUDIO_PATH = "../test_audio.wav" # Relative to dara-backend/
OUTPUT_AUDIO_PATH = "response_audio.wav"

def test_backend():
    print(f"🚀 Starting Backend Test...")
    print(f"📂 Reading audio from: {TEST_AUDIO_PATH}")
    
    if not os.path.exists(TEST_AUDIO_PATH):
        print(f"❌ Error: Test audio file not found at {TEST_AUDIO_PATH}")
        return

    try:
        # Load audio
        with open(TEST_AUDIO_PATH, "rb") as f:
            audio_bytes = f.read()
        
        print(f"📡 Sending request to {API_URL}...")
        
        # Send POST request
        files = {"audio": ("test_audio.wav", audio_bytes, "audio/wav")}
        response = requests.post(API_URL, files=files)
        
        if response.status_code == 200:
            print("✅ Success! Response received.")
            data = response.json()
            
            # Print details
            print("\n--- 📝 Response Details ---")
            print(f"🗣️  Transcript: {data.get('transcript')}")
            print(f"🌍 Language:   {data.get('language')}")
            
            intent = data.get('intent', {})
            print(f"🧠 Intent:     {intent.get('type')}")
            print(f"🔧 Action:     {intent.get('action')}")
            print(f"🔦 Device:     {intent.get('device')}")
            print(f"🤖 Response:   {intent.get('response_text')}")
            
            # Save audio response
            audio_b64 = data.get('response_audio')
            if audio_b64:
                print("\n💾 Saving response audio...")
                audio_data = base64.b64decode(audio_b64)
                with open(OUTPUT_AUDIO_PATH, "wb") as f:
                    f.write(audio_data)
                print(f"✅ Saved response to: {os.path.abspath(OUTPUT_AUDIO_PATH)}")
                print(f"👉 You can play this file to hear the response!")
            else:
                print("⚠️ No audio response received.")
                
        else:
            print(f"❌ Request failed with status code: {response.status_code}")
            print(f"Error: {response.text}")

    except Exception as e:
        print(f"❌ Exception occurred: {e}")

if __name__ == "__main__":
    test_backend()
