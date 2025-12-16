import os
import sys
from dotenv import load_dotenv
from spitch import Spitch

load_dotenv()

api_key = os.getenv("SPITCH_API_KEY")
if not api_key:
    print("Error: SPITCH_API_KEY not found in .env")
    sys.exit(1)

print(f"Using API Key: {api_key[:4]}...{api_key[-4:]}")

client = Spitch(api_key=api_key)

print("\n--- Testing Spitch API ---")
tests = [
    {"text": "Hello", "language": "en", "voice": "sade", "desc": "Default (sade/en)"},
    {"text": "Hello", "language": "en", "voice": "funmi", "desc": "Alternative Voice (funmi)"},
    {"text": "Sannu", "language": "ha", "voice": "amina", "desc": "Hausa (amina)"},
    # {"text": "Hello", "language": "en", "voice": "sade", "model": "legacy", "desc": "Legacy Model"}, # try legacy if supported
]

for t in tests:
    print(f"\n--- Testing: {t['desc']} ---")
    try:
        # Construct args dynamically
        kwargs = {k: v for k,v in t.items() if k != "desc"}
        kwargs["format"] = "mp3" # Keep format for consistency
        
        res = client.speech.generate(**kwargs)
        print(f"✅ Success! Size: {len(res.content)}")
    except Exception as e:
        print(f"❌ Failed: {e}")

