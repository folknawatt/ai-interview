"""Audio processing utilities for the AI Interview system.

This module provides core functionality for audio processing tasks including:
- Audio transcription using Typhoon ASR
- Audio extraction from video files using ffmpeg
- Splitting audio files into overlapping chunks for processing
"""

import math
import os
import subprocess
import tempfile
from pathlib import Path

from typhoon_asr import transcribe

from app.config.logging_config import get_logger
from app.exceptions import TranscriptionError

logger = get_logger(__name__)


def transcribe_audio(audio_path: str) -> str:
    """Transcribes audio using the Typhoon ASR model.

    Args:
        audio_path (str): Path to the audio file.

    Returns:
        str: The transcribed text.

    Raises:
        FileNotFoundError: If audio file doesn't exist.
        TranscriptionError: If transcription fails for any reason.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    logger.info("Transcribing audio: %s", audio_path)

    try:
        result_no_timestamps = transcribe(audio_path, with_timestamps=False, device="auto")

        # Extract text from typhoon_asr result
        # The library can return different formats depending on version/settings
        try:
            if isinstance(result_no_timestamps, list):
                # typhoon_asr returns list when with_timestamps=False
                if result_no_timestamps:
                    # Check if list contains strings or objects with .text
                    first_item = result_no_timestamps[0]
                    if isinstance(first_item, str):
                        # List of strings - join them
                        text = " ".join(result_no_timestamps)
                    elif hasattr(first_item, "text"):
                        # List of objects with .text attribute
                        text = " ".join(
                            item.text if hasattr(item, "text") else str(item)
                            for item in result_no_timestamps
                        )
                    else:
                        # Unknown list format - convert to strings and join
                        text = " ".join(str(item) for item in result_no_timestamps)
                else:
                    text = ""
            elif isinstance(result_no_timestamps, dict):
                # Handle dict format
                text_value = result_no_timestamps.get("text", "")
                if hasattr(text_value, "text"):
                    text = text_value.text
                else:
                    text = str(text_value) if text_value else ""
            elif isinstance(result_no_timestamps, str):
                # Direct string result
                text = result_no_timestamps
            else:
                # Fallback: try to get text attribute or convert to string
                if hasattr(result_no_timestamps, "text"):
                    text = result_no_timestamps.text
                else:
                    text = str(result_no_timestamps)
        except (AttributeError, KeyError, TypeError, IndexError) as e:
            logger.error("Error accessing transcription result structure: %s", e)
            logger.error("Result type: %s", type(result_no_timestamps))
            logger.error("Result value: %s", result_no_timestamps)
            raise TranscriptionError(
                f"Failed to extract text from transcription result: {str(e)}"
            ) from e

        if not text or not text.strip():
            raise TranscriptionError("Transcription returned empty text")

        logger.info("Transcription successful, length: %d characters", len(text))
        return text.strip()

    except ImportError as e:
        logger.error("typhoon_asr library not available: %s", e)
        raise TranscriptionError(
            "Transcription unavailable: typhoon_asr not installed or "
            "not compatible with this system"
        ) from e
    except TranscriptionError:
        # Re-raise TranscriptionError as-is
        raise
    except Exception as e:
        logger.error("Unexpected transcription error: %s", e, exc_info=True)
        raise TranscriptionError(f"Transcription failed: {str(e)}") from e


def extract_audio(video_path: str, output_audio_path: str | None = None) -> str:
    """Extracts audio from a video file using ffmpeg.

    Args:
        video_path (str): Path to the input video file.
        output_audio_path (Optional[str]): Path to save the extracted
            audio. If None, a temporary file is created.

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

    logger.info("Extracting audio from %s to %s", video_path, output_audio_path)

    command = [
        "ffmpeg",
        "-y",  # Overwrite output file without asking
        "-i",
        video_path,
        "-vn",  # Disable video recording
        "-acodec",
        "libmp3lame",  # Force mp3 encoding
        "-q:a",
        "2",  # Good quality
        output_audio_path,
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)  # noqa: S603, S607
        logger.info("Audio extraction successful.")
    except subprocess.CalledProcessError as e:
        logger.error("ffmpeg failed: %s", e.stderr)
        raise RuntimeError(f"ffmpeg failed to extract audio: {e.stderr}") from e
    except FileNotFoundError as exc:
        logger.error("ffmpeg not found. Please install ffmpeg.")
        raise RuntimeError(
            "ffmpeg not found. Please ensure ffmpeg is installed and in your PATH."
        ) from exc

    return output_audio_path


# ---------------Audio splitting---------------


def get_audio_duration(path: str) -> float:
    """Get the duration of an audio file in seconds.

    Args:
        path: Path to the audio file.

    Returns:
        Duration in seconds.

    Raises:
        FileNotFoundError: If audio file doesn't exist.
        subprocess.CalledProcessError: If ffprobe fails.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Audio file not found: {path}")

    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                path,
            ],
            capture_output=True,
            text=True,
            check=True,
        )  # noqa: S603, S607
        duration = float(result.stdout.strip())
        logger.info("Audio duration: %s seconds", duration)
        return duration
    except subprocess.CalledProcessError as e:
        logger.error("Failed to get audio duration: %s", e.stderr)
        raise


def run_ffmpeg_split(cmd: list[str], chunk_index: int):
    """Helper function to execute FFmpeg command."""
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # noqa: S603, S607
    except subprocess.CalledProcessError as e:
        logger.error("Failed to create chunk %d: %s", chunk_index, e)
        raise


def split_audio_with_overlap(
    input_path: str, output_dir: str, chunk_len: int = 3600, overlap_len: float | None = None
) -> list[str]:
    """Split audio file into overlapping chunks using FFmpeg.

    This function divides a long audio file into smaller chunks with overlap
    to ensure continuity in transcription. The overlap prevents words from
    being cut off at chunk boundaries.

    Args:
        input_path: Path to the input audio file.
        output_dir: Directory to save audio chunks.
        chunk_len: Duration of each chunk in seconds (Default: 3600).
        overlap_len: Overlap duration in seconds (Default: 5% of chunk_len).

    Returns:
        List of paths to the created chunk files.

    Raises:
        ValueError: If overlap is too large relative to chunk duration.
        subprocess.CalledProcessError: If FFmpeg fails.
    """
    if overlap_len is None:
        overlap_len = chunk_len * 0.05

    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)

    # Get total audio duration
    total_duration = get_audio_duration(input_path)
    if total_duration == 0:
        logger.warning("Audio file has zero duration")
        return []

    # Calculate step size (how much to advance for each chunk)
    step = chunk_len - overlap_len

    # Validate that overlap is not too large
    if step <= 0:
        raise ValueError(
            f"Overlap ({overlap_len:.2f}s) is too large for chunk "
            f"duration ({chunk_len}s). Step size must be positive."
        )

    # Calculate number of chunks needed
    num_chunks = math.ceil(total_duration / step)

    logger.info("📂 Total audio duration: %s seconds", total_duration)
    logger.info(
        "🔪 Splitting into %d chunks of %s seconds with %s seconds overlap",
        num_chunks,
        chunk_len,
        overlap_len,
    )

    # Extract base filename and extension
    file_name_base = Path(input_path).stem
    ext = Path(input_path).suffix

    chunk_files = []

    for i in range(num_chunks):
        # Calculate start time for this chunk
        start_time = i * step
        logger.debug("Chunk %d start time: %s", i, start_time)

        # Calculate actual segment duration (may be shorter for last chunk)
        segment_duration = chunk_len
        if start_time + chunk_len > total_duration:
            segment_duration = total_duration - start_time

        # Generate output path
        output_path = os.path.join(output_dir, f"{file_name_base}_overlap_{i:03d}{ext}")
        chunk_files.append(output_path)

        logger.info("   [Chunk %03d] Start: %s, Duration: %s", i, start_time, segment_duration)

        # Build FFmpeg command
        cmd = [
            "ffmpeg",
            "-y",
            "-ss",
            str(start_time),
            "-t",
            str(segment_duration),
            "-i",
            input_path,
            "-c",
            "copy",
            output_path,
        ]

        # Execute FFmpeg
        run_ffmpeg_split(cmd, i)

        # Stop if we've reached the end of the file
        if start_time + segment_duration >= total_duration:
            break

    logger.info("✅ Created %d audio chunks", len(chunk_files))
    return chunk_files
