import os
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
from django.conf import settings
from .progress import update_progress
def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    audio = sr.AudioFile(audio_path)
    
    with audio as source:
        audio_data = recognizer.record(source)
        
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def save_transcription_to_file(transcription, file_path):
    with open(file_path, 'w') as file:
        file.write(transcription)

def translate_text(text, src_language='en', dest_language='hi'):
    translator = Translator()
    translation = translator.translate(text, src=src_language, dest=dest_language)
    return translation.text

def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_text_to_file(text, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def clean_text(text):
    return text.strip()

def convert_text_to_speech(text, output_audio_file, lang='hi'):
    text = clean_text(text)
    if not text:
        print("No valid text to convert.")
        return

    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(output_audio_file)
        
        if not os.path.exists(output_audio_file):
            print(f"Output file {output_audio_file} was not created.")
        else:
            print(f"Audio file saved successfully as {output_audio_file}")
    
    except Exception as e:
        print(f"Error converting text to speech: {e}")

def replace_audio(video_path, new_audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    new_audio_clip = AudioFileClip(new_audio_path)
    video_clip = video_clip.set_audio(new_audio_clip)
    video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

def process_video(video_file_path, language='hi'):
    video_path = os.path.join(settings.MEDIA_ROOT, video_file_path)
    extracted_audio_path = os.path.join(settings.MEDIA_ROOT, 'extracted_audio.wav')
    transcription_file_path = os.path.join(settings.MEDIA_ROOT, 'transcription.txt')
    translation_file_path = os.path.join(settings.MEDIA_ROOT, 'translated_transcriptions.txt')
    translated_audio_file_path = os.path.join(settings.MEDIA_ROOT, 'translated_audio.mp3')
    output_video_path = os.path.join(settings.MEDIA_ROOT, 'output_dubbed_video.mp4')

    # Update progress
    update_progress('audio_extraction', 10)
    extract_audio_from_video(video_path, extracted_audio_path)

    # Update progress
    update_progress('transcription', 30)
    transcription_result = transcribe_audio(extracted_audio_path)
    if transcription_result:
        save_transcription_to_file(transcription_result, transcription_file_path)
        
        # Update progress
        update_progress('translation', 50)
        text_to_translate = read_text_from_file(transcription_file_path)
        if text_to_translate:
            translated_text = translate_text(text_to_translate, dest_language=language)
            write_text_to_file(translated_text, translation_file_path)
            
            # Update progress
            update_progress('text_to_speech', 70)
            text = read_text_from_file(translation_file_path)
            if text:
                convert_text_to_speech(text, translated_audio_file_path, lang=language)
                
                # Update progress
                update_progress('merging', 90)
                replace_audio(video_path, translated_audio_file_path, output_video_path)

    # Final progress update
    update_progress('completed', 100)
    return 'output_dubbed_video.mp4'