import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

async def transcribe(audio_bytes: bytes) -> tuple[str, str]:
    """
    Transcribe audio using Deepgram Nova-2 model (Async).
    Returns: (transcript, detected_language_code)
    """
    if not DEEPGRAM_API_KEY:
        print("Error: DEEPGRAM_API_KEY not found in environment variables.")
        return "", "en"
    
    # Deepgram API URL
    # model=nova-2: Fastest and most accurate
    # detect_language=true: Auto-detect language
    # smart_format=true: Punctuation and formatting
    url = "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true&detect_language=true"
    
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/wav" # We transmit consistent WAV from audio_utils
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, content=audio_bytes, headers=headers, timeout=10.0)
            # Debug Deepgram response
            if response.status_code != 200:
                print(f"Deepgram Error Status: {response.status_code}")
                print(f"Deepgram Error Body: {response.text}")
            
            response.raise_for_status()
            data = response.json()
            
            # Print full debug response to see what's happening
            # print(f"DEBUG Deepgram: {data}")

            # Parse result
            results = data.get("results", {})
            channels = results.get("channels", [{}])
            alternatives = channels[0].get("alternatives", [{}])
            
            result = alternatives[0]
            transcript = result.get("transcript", "")
            confidence = result.get("confidence", 0.0)
            
            if not transcript:
                print(f"DEBUG: Empty transcript from Deepgram. Confidence: {confidence}")
            
            # Deepgram language detection (if enabled)
            # detect_language=true returns 'detected_language' in the channel or alternative?
            # It seems to be in data['results']['channels'][0]['detected_language']
            language = channels[0].get("detected_language", "en")
            
            return transcript, language
            
        except Exception as e:
            print(f"Deepgram STT Error: {str(e)}")
            return "", "en"
