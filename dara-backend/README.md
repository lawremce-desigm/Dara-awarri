# Dára Home Backend (Multilingual 🇳🇬)

Production-quality backend for the Dára Home voice assistant, featuring native support for Nigerian languages.

## Architecture

| Component | Technology | Purpose |
|---|---|---|
| **STT** | **OpenAI Whisper** | Robust speech recognition for Nigerian accents (En, Yo, Ha, Ig). |
| **Reasoning** | **NCAIR1/N-ATLaS (Modal)** | The actual N-ATLaS model deployed on Modal.co for intent classification. |
| **TTS** | **Spitch** | High-quality, native African text-to-speech. |

### Language Support Matrix

| Language | Code | STT | Reasoning | TTS (Spitch Voice) |
|---|---|---|---|---|
| English | `en` | ✅ | ✅ | ✅ (`lucy`) |
| Yoruba | `yo` | ✅ | ✅ | ✅ (`sade`) |
| Hausa | `ha` | ✅ | ✅ | ✅ (`amina`) |
| Igbo | `ig` | ✅ | ✅ | ✅ (`ngozi`) |

### Data Flow
1.  **Audio Input**: `POST /voice` accepts mp3, mp4, wav, m4a.
2.  **Normalization**: Converts payload to 16kHz WAV.
3.  **Transcription**: OpenAI Whisper detects language and transcribes text.
4.  **Reasoning**: NCAIR1/N-ATLaS (deployed on Modal) receives text + language, determines intent, and generates a response *in the same language*.
5.  **Synthesis**: Spitch generates the spoken response using native African voices.
6.  **Response**: JSON payload with intent, language metadata, and base64 audio.

## Setup

1.  **Clone & CD**:
    ```bash
    cd dara-backend
    ```

2.  **Environment Variables**:
    Rename `.env.example` to `.env` and fill in keys.
    ```bash
    cp .env.example .env
    ```
    *   `HF_TOKEN`: Hugging Face User Access Token.
    *   `OPENAI_API_KEY`: OpenAI API Key.
    *   `SPITCH_API_KEY`: Spitch API Key.

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *   Ensure `ffmpeg` is installed.

## Running Locally

```bash
uvicorn main:app --reload
```
Server running at `http://localhost:8000`.

## Testing

### Using Postman
*   **Method**: `POST`
*   **URL**: `http://localhost:8000/voice`
*   **Body**: form-data -> `audio` (File)

### Example Response (Yoruba)
```json
{
  "transcript": "Tan ina",
  "language": "yo",
  "intent": {
    "type": "INSTRUCTION",
    "language": "yo",
    "action": "TURN_ON",
    "device": "LIGHT",
    "response_text": "Mo ti tan ina."
  },
  "response_audio": "UklGRi..."
}
```
