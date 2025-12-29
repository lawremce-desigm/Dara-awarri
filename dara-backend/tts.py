import os
import asyncio
import logging
from typing import Optional
from dotenv import load_dotenv
from spitch import Spitch

# --------------------------------------------------
# ENV SETUP
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# LOGGING
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --------------------------------------------------
# SPITCH CLIENT
# --------------------------------------------------
spitch_client: Optional[Spitch] = None

try:
    api_key = os.getenv("SPITCH_API_KEY")
    if api_key:
        spitch_client = Spitch(api_key=api_key)
        logger.info("Spitch client initialized")
    else:
        logger.error("SPITCH_API_KEY not found in .env")
except Exception as e:
    logger.error(f"Spitch initialization failed: {e}")

# --------------------------------------------------
# VOICE MAP
# --------------------------------------------------
# All female voices as requested
VOICE_MAP = {
    "en": {"voice": "lucy", "language": "en"},
    "ha": {"voice": "amina", "language": "ha"},
    "yo": {"voice": "sade", "language": "yo"},
    "ig": {"voice": "ngozi", "language": "ig"},
}

# --------------------------------------------------
# SPITCH TTS (SYNC – RUNS IN THREAD)
# --------------------------------------------------
def _generate_spitch_tts_sync(text: str, language: str) -> Optional[bytes]:
    try:
        if not spitch_client:
            logger.error("Spitch client is not initialized")
            return None

        # Default to English/lucy if language not supported
        config = VOICE_MAP.get(language, VOICE_MAP["en"])
        
        logger.info(f"generating audio for language {language} with voice {config['voice']}")

        response = spitch_client.speech.generate(
            text=text,
            language=config["language"],
            voice=config["voice"],
            format="mp3"
        )
        
        # BinaryAPIResponse handling
        content = None
        if hasattr(response, 'content'):
            content = response.content
        elif hasattr(response, 'read'):
            content = response.read()

        return content

    except Exception as e:
        logger.error(f"Spitch TTS error: {e}")
        return None


# --------------------------------------------------
# PUBLIC API
# --------------------------------------------------
async def generate_audio(text: str, language: str = "en") -> bytes:
    """
    Generate speech audio using Spitch API.
    
    Args:
        text: The text to convert to speech
        language: Language code ('en', 'ha', 'yo', 'ig')
        
    Returns:
        MP3 bytes or empty bytes on failure
    """

    if not text.strip():
        return b""

    if spitch_client:
        logger.info(f"Generating Spitch TTS ({language})")
        audio = await asyncio.to_thread(
            _generate_spitch_tts_sync, text, language
        )
        if audio:
            logger.info(f"Spitch TTS success ({len(audio)} bytes)")
            return audio

        logger.warning("Spitch TTS returned no audio")

    return b""


# --------------------------------------------------
# LOCAL TEST
# --------------------------------------------------
if __name__ == "__main__":
    async def test():
        print("Testing English...")
        audio = await generate_audio(
            "Hello, this is a test of Spitch English.",
            language="en",
        )
        if audio:
            with open("test_spitch_en.mp3", "wb") as f:
                f.write(audio)
            print("Saved test_spitch_en.mp3")
        else:
            print("Failed to generate English audio")

        print("\nTesting Igbo...")
        audio_ig = await generate_audio(
            "Kedu, kedu ka i mere?",
            language="ig",
        )
        if audio_ig:
            with open("test_spitch_ig.mp3", "wb") as f:
                f.write(audio_ig)
            print("Saved test_spitch_ig.mp3")
        else:
            print("Failed to generate Igbo audio")

    asyncio.run(test())
