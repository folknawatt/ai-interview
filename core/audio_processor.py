# core/audio_processor.py
import os
import logging
import tempfile
import subprocess
import streamlit as st
from typing import Optional
from typhoon_asr import transcribe


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='my_app.log',  # <--- ระบุชื่อไฟล์ตรงนี้
    # 'a' = append (ต่อท้าย), 'w' = write (ทับใหม่ทุกครั้ง)
    filemode='a'
)
logger = logging.getLogger(__name__)


def extract_audio(video_path: str, output_audio_path: Optional[str] = None) -> str:
    """
    Extracts audio from a video file using ffmpeg.

    Args:
        video_path (str): Path to the input video file.
        output_audio_path (Optional[str]): Path to save the extracted audio. 
                                           If None, a temporary file is created.

    Returns:
        str: Path to the extracted audio file.

    Raises:
        RuntimeError: If ffmpeg fails to extract audio.
        FileNotFoundError: If the video file does not exist.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    if output_audio_path is None:
        # Create a temporary file for the audio
        fd, output_audio_path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)  # Close the file descriptor, we just need the path

    logger.info("Extracting audio from %s to %s",
                video_path, output_audio_path)

    command = [
        "ffmpeg",
        "-y",  # Overwrite output file without asking
        "-i", video_path,
        "-vn",  # Disable video recording
        "-acodec", "libmp3lame",  # Force mp3 encoding
        "-q:a", "2",  # Good quality
        output_audio_path
    ]

    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("Audio extraction successful.")
    except subprocess.CalledProcessError as e:
        logger.error("ffmpeg failed: %s", e.stderr)
        raise RuntimeError(
            f"ffmpeg failed to extract audio: {e.stderr}") from e
    except FileNotFoundError as exc:
        logger.error("ffmpeg not found. Please install ffmpeg.")
        raise RuntimeError(
            "ffmpeg not found. Please ensure ffmpeg is installed and in your PATH.") from exc

    return output_audio_path


@st.cache_data(show_spinner=False)
def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes audio using the Typhoon ASR model.
    Results are cached by Streamlit to avoid re-running for the same file.

    Args:
        audio_path (str): Path to the audio file.

    Returns:
        str: The transcribed text.

    Raises:
        RuntimeError: If transcription fails.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    logger.info("Transcribing audio: %s", audio_path)

    try:
        # Note: typhoon_asr.transcribe seems to load the model internally or globally.
        # If it's heavy to load, we might need a separate model loader,
        # but based on previous code it was just calling transcribe.
        result_no_timestamps = transcribe(
            audio_path, with_timestamps=False, device="cuda"
        )
        text = result_no_timestamps["text"].text
        logger.info("Transcription successful.")
        return text
    except Exception as e:
        logger.error("Transcription failed: %s", e)
        raise RuntimeError(f"Transcription failed: {e}") from e
