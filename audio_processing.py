import noisereduce as nr
import librosa
from jiwer import wer
import soundfile as sf
import os
import numpy as np
import whisperx

# Load WhisperX model
def get_model():
    device = "cpu"
    return whisperx.load_model("base", device=device, compute_type="float32")

def calculate_rms(y):
    # Calculate RMS (Root Mean Square) value of the audio signal
    rms = librosa.feature.rms(y=y)
    return np.mean(rms)

def fast_noise_reduction(file):
    # Load audio in mono, 16kHz
    y, sr = librosa.load(file, sr=16000, mono=True)
    rms_before = calculate_rms(y)
    # Perform fast noise reduction
    reduced = nr.reduce_noise(y=y, sr=sr, prop_decrease=0.7)
    
    rms_after = calculate_rms(reduced)
    reduction_percentage = ((rms_before - rms_after) / rms_before) * 100
    print(f"Noise Reduction Percentage: {reduction_percentage:.2f}%")
    
    denoised_file = f"{os.path.splitext(file)[0]}_denoised.wav"
    sf.write(denoised_file, reduced, sr, subtype='PCM_16')
    
    return denoised_file

def transcribe(audio_path):
    model = get_model()
    # Automatically detect language with WhisperX
    result = model.transcribe(audio_path, language="en")
    return " ".join([seg['text'] for seg in result.get('segments', [])])

def process(file):
    denoised_file = fast_noise_reduction(file)

    # original_text = transcribe(file)
    cleaned_text = transcribe(denoised_file)
    return cleaned_text

    # print("Original Text:", original_text)
    # print("Denoised Text:", cleaned_text)
    # print(f"Original WER: {wer(ref, original_text) * 100:.2f}%")
    # print(f"Denoised WER: {wer(ref, cleaned_text) * 100:.2f}%")

# Run your test
# test("test1.wav", "Show me summary of my last five rides.")
