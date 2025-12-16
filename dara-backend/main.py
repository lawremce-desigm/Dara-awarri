from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import StreamingResponse
import uvicorn
import io
import base64
import time
import logging
import audio_utils
import stt_whisper as stt_service # Reverted to Whisper
import reasoning
import tts
from schemas import VoiceResponse

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Dára Home Backend")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Path: {request.url.path} Method: {request.method} Time: {process_time:.4f}s Status: {response.status_code}")
    return response

@app.post("/voice", response_model=VoiceResponse)
async def process_voice(audio: UploadFile = File(...)):
    """
    Core endpoint for Dára Home.
    Accepts audio file, returns transcript, intent, and base64 audio response.
    """
    # 1. Validate file type
    if not audio.content_type.startswith("audio/") and not audio.filename.lower().endswith(('.mp3', '.mp4', '.wav', '.m4a')):
        # Log warning but proceed if possible, or raise
        pass

    try:
        t0 = time.time()
        
        # Read audio content
        audio_bytes = await audio.read()
        logger.info(f"Received audio: {len(audio_bytes)} bytes. Filename: {audio.filename} Content-Type: {audio.content_type}")

        if len(audio_bytes) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file received.")
        
        # 2. Normalize audio (Async)
        wav_bytes = await audio_utils.convert_to_wav(audio_bytes)
        logger.info(f"Converted WAV size: {len(wav_bytes)} bytes")
        t1 = time.time()
        
        # 3. Speech to Text (Async - Deepgram)
        transcript, language = await stt_service.transcribe(wav_bytes)
        t2 = time.time()
        logger.info(f"STT: '{transcript}' ({language}) [{t2-t1:.4f}s]")
        
        # 4. Reasoning (Async)
        reasoning_result = await reasoning.classify_intent(transcript, language)
        intent = reasoning_result["intent"]
        response_text = reasoning_result["response_text"]
        t3 = time.time()
        logger.info(f"Intent: {intent.type} Action: {intent.action} Device: {intent.device} [{t3-t2:.4f}s]")
        
        # 5. Text to Speech (Async)
        response_lang = intent.language or language
        response_audio_bytes = await tts.generate_audio(response_text, response_lang)
        t4 = time.time()
        logger.info(f"TTS: Generated {len(response_audio_bytes)} bytes (raw) [{t4-t3:.4f}s]")
        
        logger.info(f"Total Processing Time: {t4-t0:.4f}s")
        
        # 6. Return Response
        response_audio_b64 = base64.b64encode(response_audio_bytes).decode("utf-8")
        
        return VoiceResponse(
            transcript=transcript,
            language=response_lang,
            intent=intent,
            response_audio=response_audio_b64
        )

    except Exception as e:
        logger.error(f"Processing Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/voice/audio")
async def process_voice_audio(audio: UploadFile = File(...)):
    """
    Test endpoint that returns MP3 audio directly.
    """
    try:
        audio_bytes = await audio.read()
        wav_bytes = await audio_utils.convert_to_wav(audio_bytes)
        transcript, language = await stt_service.transcribe(wav_bytes)
        
        reasoning_result = await reasoning.classify_intent(transcript, language)
        intent = reasoning_result["intent"]
        response_text = reasoning_result["response_text"]
        
        response_lang = intent.language or language
        response_audio_base64 = await tts.generate_audio(response_text, response_lang)
        
        # Decode base64 to raw MP3 bytes
        audio_mp3 = base64.b64decode(response_audio_base64)
        
        return StreamingResponse(
            io.BytesIO(audio_mp3),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=response.mp3",
                "X-Transcript": transcript,
                "X-Language": language
            }
        )

    except Exception as e:
        logger.error(f"Processing Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
