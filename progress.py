import os
import subprocess
import torch
from TTS.api import TTS
from pydub import AudioSegment
import speech_recognition as sr
from translate import Translator
import noisereduce as nr
from moviepy.editor import VideoFileClip

# Path to FFmpeg
ffmpeg_path = "D:\\ffmpeg.exe"

def remove_background_noise(audio_file):
    audio = AudioSegment.from_wav(audio_file)
    reduced_noise = nr.reduce_noise(audio.get_array_of_samples(), audio.frame_rate)
    cleaned_audio = AudioSegment(
        data=reduced_noise.tobytes(),
        sample_width=audio.sample_width,
        frame_rate=audio.frame_rate,
        channels=audio.channels
    )
    cleaned_audio.export("vocals.wav", format="wav")
    return "vocals.wav"

def transcribe_and_translate_audio(audio_path, input_language='en', target_language='en'):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data, language=input_language)
        translator = Translator(to_lang=target_language)
        translated_text = translator.translate(text)
        return translated_text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)

def process_video(input_video_path, input_language='en', target_language='en'):
    if not os.path.exists(input_video_path):
        print("File not found.")
        return None, []

    subprocess.run([ffmpeg_path, "-i", input_video_path, "-c:v", "copy", "only_video.mp4"])
    subprocess.run([ffmpeg_path, "-i", input_video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "only_audio.wav"])
    cleaned_audio_file = remove_background_noise("only_audio.wav")
    print(f"Background noise removed. Cleaned audio saved as '{cleaned_audio_file}'")

    audio_chunks = []
    for i in range(0, len(AudioSegment.from_wav(cleaned_audio_file)), 50000):
        chunk = AudioSegment.from_wav(cleaned_audio_file)[i:i + 50000]
        chunk.export(f"chunk{i}.wav", format="wav")
        audio_chunks.append(f"chunk{i}.wav")

    text_chunks = []
    for chunk_path in audio_chunks:
        text = transcribe_and_translate_audio(chunk_path, input_language=input_language, target_language=target_language)
        text_chunks.append(text)
    
    return "only_video.mp4", text_chunks

def generate_speech(text_chunks, audio_chunks):
    combined_audio = AudioSegment.empty()
    for i, chunk_path in enumerate(audio_chunks):
        if i < len(text_chunks):
            text = text_chunks[i]
            output_path = f"output_{os.path.basename(chunk_path)}"
            tts.tts_to_file(text=text, speaker_wav=chunk_path, language="hi", file_path=output_path)
            combined_audio += AudioSegment.from_wav(output_path)
        else:
            print(f"Missing text for audio chunk: {chunk_path}")
    combined_audio.export("combined_output.wav", format="wav")
    return "combined_output.wav"

def merge_video_and_audio(video_path, audio_path):
    # Load video clip to get duration
    video_clip = VideoFileClip(video_path)
    video_duration = video_clip.duration  # Duration in seconds
    video_clip.close()

    # Get audio duration
    audio_duration = len(AudioSegment.from_wav(audio_path)) / 1000  # Duration in seconds

    # Adjust audio duration to match video duration if necessary
    if audio_duration > video_duration:
        audio = AudioSegment.from_wav(audio_path)
        audio = audio[:int(video_duration * 1000)]  # Trim to match video duration
        audio.export("adjusted_audio.wav", format="wav")
        audio_path = "adjusted_audio.wav"

    # Trim video to match audio length if necessary
    if video_duration > audio_duration:
        subprocess.run([ffmpeg_path, "-i", video_path, "-ss", "0", "-t", str(audio_duration), "-c:v", "copy", "trimmed_video.mp4"])
        video_path = "trimmed_video.mp4"

    # Merge video and audio
    subprocess.run([ffmpeg_path, "-i", video_path, "-i", audio_path, "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", "-map", "0:v:0", "-map", "1:a:0", "Final_output.mp4"])
    
    # Clean up temporary files
    if os.path.exists("adjusted_audio.wav"):
        os.remove("adjusted_audio.wav")
    if os.path.exists("trimmed_video.mp4"):
        os.remove("trimmed_video.mp4")

    return "Final_output.mp4"
