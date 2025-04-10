import noisereduce as nr
import librosa
from jiwer import wer, Compose, RemovePunctuation, ToLowerCase, RemoveWhiteSpace
import streamlit as st
import soundfile as sf
import os
from pydub import AudioSegment
import whisper

model = whisper.load_model("base")

transformation = Compose([
    RemovePunctuation(),
    ToLowerCase(),
    RemoveWhiteSpace()
])

def noiseReduction(file):
    sound = AudioSegment.from_file(file)
    sound = sound.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    sound.export(file, format="wav")

    # Load noisy audio
    y, sr_rate = librosa.load(file, sr=None)

    # Apply noise reduction
    reduced_noise = nr.reduce_noise(y=y, sr=sr_rate)

    # Save clean audio (proper PCM WAV)
    output_file = f"{os.path.splitext(os.path.basename(file))[0]}_denoised.wav"
    sf.write(output_file, reduced_noise, sr_rate, subtype='PCM_16')

def transcribe(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]

def test(file, ref):
    noiseReduction(file)

    original_text = transcribe(file)
    cleaned_text = transcribe(f"{os.path.splitext(os.path.basename(file))[0]}_denoised.wav")

    # Normalize all texts
    norm_ref = transformation(ref)
    norm_original = transformation(original_text)
    norm_cleaned = transformation(cleaned_text)

    print("Original Text:", original_text)
    print("Denoised Text:", cleaned_text)
    print(f"Original Error Percentage: {wer(norm_ref, norm_original)*100:.2f}%")
    print(f"Denoised Error Percentage: {wer(norm_ref, norm_cleaned)*100:.2f}%")

test("test3.wav", "Show me the summary of my first 5 rides")
