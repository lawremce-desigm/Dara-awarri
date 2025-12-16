import os
import io
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def transcribe(audio_bytes: bytes) -> tuple[str, str]:
    """
    Sends audio bytes to OpenAI Whisper API (Async).
    Returns: (transcript, detected_language_code)
    """
    try:
        # OpenAI API requires a file-like object with a name
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.wav"

        transcript_response = await client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json"
        )
        
        # verbose_json returns an object with 'text' and 'language'
        text = transcript_response.text
        language = transcript_response.language
        
        return text, language

    except Exception as e:
        print(f"STT Error: {e}")
        return "", "en"
