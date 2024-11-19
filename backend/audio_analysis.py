import os, logging, requests, replicate
from uuid import uuid4
from moviepy.editor import VideoFileClip

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


async def analyse_audio(video_url: str) -> str:
    logger.info("Analyzing audio from video URL: %s", video_url)

    # Generate unique filenames for video and audio
    random_name = str(uuid4())
    video_path = f"./videos/{random_name}.mp4"
    audio_path = f"./audios/{random_name}.mp3"

    # Download video from URL
    try:
        response = requests.get(video_url, timeout=30)
        if response.status_code != 200:
            logger.error(
                "Failed to download video. Status code: %d", response.status_code
            )
            return "Invalid video URL"

        os.makedirs(os.path.dirname(video_path), exist_ok=True)
        with open(video_path, "wb") as file:
            file.write(response.content)
        logger.info("Downloaded video to: %s", video_path)
    except requests.RequestException as e:
        logger.error("Error downloading video: %s", e)
        return "Failed to download video"

    # Extract audio from video
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        audio_clip.write_audiofile(audio_path)
        logger.info("Extracted audio to: %s", audio_path)
    except Exception as e:
        logger.error("Error extracting audio from video: %s", e)
        cleanup_files(video_path, audio_path)
        return "No audio found"
    finally:
        video_clip.close()

    # Analyze audio using Replicate's Whisper model
    try:
        with open(audio_path, "rb") as audio_file:
            output = replicate.run(
                "openai/whisper:cdd97b257f93cb89dede1c7584e3f3dfc969571b357dbcee08e793740bedd854",
                input={
                    "audio": audio_file,
                    "model": "large-v3",
                    "language": "auto",
                    "translate": False,
                    "temperature": 0,
                    "transcription": "vtt",
                    "suppress_tokens": "-1",
                    "logprob_threshold": -1,
                    "no_speech_threshold": 0.6,
                    "condition_on_previous_text": True,
                    "compression_ratio_threshold": 2.4,
                    "temperature_increment_on_fallback": 0.2,
                },
            )
        logger.info("Audio analysis completed for: %s", video_url)
    except Exception as e:
        logger.error("Error during audio analysis: %s", e)
        cleanup_files(video_path, audio_path)
        return "Audio analysis failed"

    # Process transcription segments
    audio_context = " ".join(seg["text"] for seg in output.get("segments", []))
    logger.info("Processed audio context: %s", audio_context)

    return audio_context

# Clean up temporary files
def cleanup_files(video_path: str, audio_path: str):
    try:
        if os.path.exists(audio_path):
            os.remove(audio_path)
            logger.info("Removed audio file: %s", audio_path)
        if os.path.exists(video_path):
            os.remove(video_path)
            logger.info("Removed video file: %s", video_path)
    except Exception as e:
        logger.warning("Error removing temporary files: %s", e)
