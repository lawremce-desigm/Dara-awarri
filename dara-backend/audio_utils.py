import subprocess
import asyncio
import io

async def convert_to_wav(audio_bytes: bytes) -> bytes:
    """
    Converts input audio bytes (mp3, mp4, wav, m4a) to 16kHz mono WAV using ffmpeg.
    
    Async wrapper for non-blocking execution.
    """
    def _sync_convert(data: bytes) -> bytes:
        try:
            # Run ffmpeg command
            # -i pipe:0  : Read from stdin
            # -ar 16000  : Sample rate 16kHz
            # -ac 1      : Mono channel
            # -f wav     : Output format WAV
            # pipe:1     : Write to stdout
            
            args = ['ffmpeg', '-y', '-i', 'pipe:0', '-ar', '16000', '-ac', '1', '-f', 'wav', 'pipe:1']
            
            process = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            out, err = process.communicate(input=data)
            
            if process.returncode != 0:
                error_msg = err.decode('utf-8')
                raise ValueError(f"FFmpeg conversion failed: {error_msg}")
                
            return out

        except Exception as e:
            if isinstance(e, FileNotFoundError):
                 raise ValueError("ffmpeg is not installed or not in PATH.")
            raise ValueError(f"Error converting audio: {str(e)}")

    # Run blocking sync function in a thread
    return await asyncio.to_thread(_sync_convert, audio_bytes)
