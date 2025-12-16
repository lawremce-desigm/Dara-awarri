import os
import asyncio
import logging
from typing import Optional


from google.cloud import texttospeech
from dotenv import load_dotenv

# --------------------------------------------------
# ENV SETUP
# --------------------------------------------------
load_dotenv()



# Requires:
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service_account.json"

# --------------------------------------------------
# LOGGING
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --------------------------------------------------

# --------------------------------------------------


# --------------------------------------------------
# GOOGLE TTS CLIENT
# --------------------------------------------------
google_tts_client: Optional[texttospeech.TextToSpeechClient] = None

try:
    google_tts_client = texttospeech.TextToSpeechClient()
    logger.info("Google TTS client initialized")
except Exception as e:
    logger.error(f"Google TTS initialization failed: {e}")

# --------------------------------------------------
# SAFE VOICE MAP (GUARANTEED TO EXIST)
# Nigerian English ≈ British Neural2
# --------------------------------------------------
GOOGLE_VOICE_MAP = {
    "en": {
        "language_code": "en-GB",
        "name": "en-GB-Neural2-A",
        "gender": texttospeech.SsmlVoiceGender.FEMALE,
    },
    "yo": {
        "language_code": "en-GB",
        "name": "en-GB-Neural2-B",
        "gender": texttospeech.SsmlVoiceGender.MALE,
    },
    "ha": {
        "language_code": "en-GB",
        "name": "en-GB-Neural2-C",
        "gender": texttospeech.SsmlVoiceGender.FEMALE,
    },
    "ig": {
        "language_code": "en-GB",
        "name": "en-GB-Neural2-D",
        "gender": texttospeech.SsmlVoiceGender.MALE,
    },
}

# --------------------------------------------------
# GOOGLE TTS (SYNC – RUNS IN THREAD)
# --------------------------------------------------
def _generate_google_tts_sync(text: str, language: str) -> Optional[bytes]:
    try:
        if not google_tts_client:
            return None

        voice_cfg = GOOGLE_VOICE_MAP.get(language, GOOGLE_VOICE_MAP["en"])

        synthesis_input = texttospeech.SynthesisInput(text=text)

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,
            pitch=0.0,
        )

        # 1️⃣ Try explicit Neural2 voice
        try:
            voice = texttospeech.VoiceSelectionParams(
                language_code=voice_cfg["language_code"],
                name=voice_cfg["name"],
                ssml_gender=voice_cfg["gender"],
            )

            response = google_tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config,
            )

            return response.audio_content

        except Exception as e:
            logger.warning(
                f"Voice {voice_cfg['name']} failed, retrying auto-select: {e}"
            )

        # 2️⃣ Retry without explicit name (auto-select)
        voice = texttospeech.VoiceSelectionParams(
            language_code=voice_cfg["language_code"],
            ssml_gender=voice_cfg["gender"],
        )

        response = google_tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config,
        )

        return response.audio_content

    except Exception as e:
        logger.error(f"Google TTS error: {e}")
        return None





# --------------------------------------------------
# PUBLIC API
# --------------------------------------------------
async def generate_audio(text: str, language: str = "en") -> bytes:
    """
    Generate speech audio.
    Priority:
      1. Google Cloud TTS (fast, cheap)
      2. OpenAI TTS (fallback)

    Returns:
      MP3 bytes
    """

    if not text.strip():
        return b""

    # 1️⃣ Google TTS
    if google_tts_client:
        logger.info(f"Generating Google TTS ({language})")
        audio = await asyncio.to_thread(
            _generate_google_tts_sync, text, language
        )
        if audio:
            logger.info(f"Google TTS success ({len(audio)} bytes)")
            return audio

        logger.warning("Google TTS returned no audio")


    return b""


# --------------------------------------------------
# LOCAL TEST
# --------------------------------------------------
if __name__ == "__main__":
    async def test():
        audio = await generate_audio(
            "Hello, this is a test of Nigerian English speech synthesis.",
            language="en",
        )

        with open("output.mp3", "wb") as f:
            f.write(audio)

        print("Saved output.mp3")

    asyncio.run(test())
