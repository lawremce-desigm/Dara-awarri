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
    # Suspected English voices
    {"text": "Hello, this is a test.", "language": "en", "voice": "john", "desc": "English (john)"},
    {"text": "Hello, this is a test.", "language": "en", "voice": "lucy", "desc": "English (lucy)"},
    
    # Hausa (seems to work conceptually)
    {"text": "Sannu", "language": "ha", "voice": "amina", "desc": "Hausa (amina)"},
    
    # Yoruba (testing likely mapping for sade)
    {"text": "Bawo ni", "language": "yo", "voice": "sade", "desc": "Yoruba (sade)"},
    
    # Igbo (Testing candidates)
    {"text": "Kedu", "language": "ig", "voice": "ngozi", "desc": "Igbo (ngozi)"},
    {"text": "Kedu", "language": "ig", "voice": "amara", "desc": "Igbo (amara)"},
]

for t in tests:
    print(f"\n--- Testing: {t['desc']} ---")
    try:
        # Construct args dynamically
        kwargs = {k: v for k,v in t.items() if k != "desc"}
        kwargs["format"] = "mp3" 
        
        res = client.speech.generate(**kwargs)
        
        # Inspect response object
        print(f"Response Type: {type(res)}")
        # Check standard attributes for binary content
        content = None
        if hasattr(res, 'content'):
            content = res.content
        elif hasattr(res, 'read'):
            content = res.read()
        elif hasattr(res, 'json'): # unlikely for binary but checking
            pass 
            
        if content:
             print(f"✅ Success! Audio size: {len(content)} bytes")
             # Save one file to verify
             filename = f"test_{t['voice']}_{t['language']}.mp3"
             with open(filename, "wb") as f:
                 f.write(content)
             print(f"   Saved to {filename}")
        else:
             print(f"⚠️  Request succeeded but could not extract content. Dir(res): {dir(res)}")

    except Exception as e:
        print(f"❌ Failed: {e}")

