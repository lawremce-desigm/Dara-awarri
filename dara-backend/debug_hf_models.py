import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def test_model(model_id):
    print(f"Testing {model_id}...")
    # Use the ROUTER url
    api_url = f"https://router.huggingface.co/hf-inference/models/{model_id}"
    
    payload = {"inputs": "Hello"}
    try:
        response = requests.post(api_url, headers=HEADERS, json=payload)
        status = response.status_code
        print(f"Status: {status}")
        if status == 200:
            print("✅ Success!")
            print(f"Response: {response.text[:100]}...")
        elif status == 403:
            print("❌ Forbidden. Possible causes:")
            print("  1. Token lacks 'Inference' permission.")
            print("  2. Model is gated (Need to accept license).")
            print("  3. Model is NOT supported on free Serverless Inference.")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")
    print("-" * 20)

def test_metadata(model_id):
    print(f"Checking metadata for {model_id}...")
    url = f"https://huggingface.co/api/models/{model_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Token has READ access.")
        elif response.status_code == 403: # actually api returns 401 usually
           print(f"❌ Forbidden (Reading Metadata). Check 'Read' permissions.")
        elif response.status_code == 401:
           print(f"❌ Unauthorized. Token invalid?")
        else:
           print(f"Response: {response.text[:100]}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)

from openai import OpenAI

def test_direct_router(model_id):
    print(f"Testing Direct Router for {model_id}...")
    # Try without 'hf-inference'
    url = f"https://router.huggingface.co/models/{model_id}"
    try:
        response = requests.post(url, headers=HEADERS, json={"inputs": "Hello"})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Success Direct Router!")
        else:
            print(f"Response: {response.text[:100]}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)

def test_openai_compat(model_id):
    print(f"Testing OpenAI Router V1 for {model_id}...")
    # Base URL for HF Router
    base_url = "https://router.huggingface.co/hf-inference/v1"
    
    # We use HF_TOKEN as the API Key
    client = OpenAI(base_url=base_url, api_key=HF_TOKEN)
    
    try:
        response = client.chat.completions.create(
            model=model_id, # Pass full model ID here
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print("✅ Success via Router V1!")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"❌ Router V1 Failed: {e}")
    print("-" * 20)

if __name__ == "__main__":
    test_openai_compat("NCAIR1/N-ATLaS")
    test_direct_router("facebook/mms-tts-eng")
