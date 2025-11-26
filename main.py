# import subprocess
from typhoon_asr import transcribe


# commands = ['ffmpeg', '-i', r'D:\ai-interview\temp_video.mp4', 'output.mp3']

# subprocess.call(commands)

# Transcription with timestamps
result_with_timestamps = transcribe(
    r"D:\ai-interview\output.mp3", with_timestamps=False, device='cuda'
)
print(result_with_timestamps['text'].text)


# from moviepy import VideoFileClip
# clip = VideoFileClip("long_examples/example2.mp4")
# clip.audio.write_audiofile("output.mp3")
