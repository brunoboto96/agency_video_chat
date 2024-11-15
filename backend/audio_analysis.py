from uuid import uuid4
from moviepy.editor import VideoFileClip
import requests, os ,replicate

def analyse_audio(video_url):
    print('Analyzing audio:', video_url)
    # Download and extract audio from video, then store in a wav file under ./audios/ with a random name
    random_name = str(uuid4())
    video_path = f'./videos/{random_name}.mp4'
    audio_path = f'./audios/{random_name}.mp3'
    
    # Get video from url
    request = requests.get(video_url)
    if request.status_code != 200:
        return "Invalid video url"
    else:
        with open(video_path, 'wb') as file:
            file.write(request.content)
        # print("Downloaded video:", video_path)
        # print("Starting audio extraction to:", audio_path)
    
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_path)
    except Exception as e:
        print("Error extracting audio:", e)
        os.remove(video_path)
        return "No audio found"
        
    finally:
        video_clip.close()
        
    
    # print("Extracted audio from video:", audio_path)
    
    audio = open(audio_path, "rb")
    output = replicate.run(
        "openai/whisper:cdd97b257f93cb89dede1c7584e3f3dfc969571b357dbcee08e793740bedd854",
        input={
            "audio": audio,
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
            "temperature_increment_on_fallback": 0.2
        }
    )
    

    # print('Prediction completed:', output)
    audio_context = ""
    for seg in output["segments"]:
        audio_context = " ".join(str(seg["text"]))
    
    
    # delete audio and video files
    os.remove(audio_path)
    os.remove(video_path)
    return audio_context
