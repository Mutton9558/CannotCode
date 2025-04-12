import noisereduce as nr
import librosa
import soundfile as sf
import os
from jiwer import wer
import whisperx
import numpy as np

device = "cpu"
model = whisperx.load_model("base", device=device, compute_type="float32")

# For testing purposes, this calculates root mean square of the audio
# def calculate_rms(y):
#     rms = librosa.feature.rms(y=y)
#     return np.mean(rms)

def noise_reduction(file, db_thresh=-40, prop_decrease=0.6):
    y, sr = librosa.load(file, sr=16000, mono=True)
    # For test purposes, this calculates root mean square of audio pre-noise reduction
    # rms_before = calculate_rms(y)
    # Step 1: Noise suppression (using noisereduce)
    y_denoised = nr.reduce_noise(y=y, sr=sr, prop_decrease=prop_decrease)
    # This calculates root mean square post noise reduction
    # rms_after = calculate_rms(y_denoised)
    # reduction_percentage = ((rms_before - rms_after) / rms_before) * 100
    # print(f"Noise Reduction Percentage: {reduction_percentage:.2f}%")

    # Step 2: Frame-wise RMS masking to cut off background noise below a certain threshold
    frame_length = 2048
    hop_length = 512

    rms = librosa.feature.rms(y=y_denoised, frame_length=frame_length, hop_length=hop_length)[0]
    rms_db = librosa.amplitude_to_db(rms)

    # Create a mask based on RMS threshold (any frame below db_thresh is considered background noise)
    mask = rms_db > db_thresh

    # Frame the signal
    frames = librosa.util.frame(y_denoised, frame_length=frame_length, hop_length=hop_length).copy()

    # Apply mask and zero out quiet frames (further background noise removal)
    for i, keep in enumerate(mask[:frames.shape[1]]):  # Limit iteration to the number of frames available
        if not keep:
            frames[:, i] = 0  # Silence frame

    # Reconstruct the signal using overlap-add
    y_filtered = np.zeros(len(y_denoised))
    for i in range(frames.shape[1]):
        start = i * hop_length
        end = start + frame_length
        y_filtered[start:end] += frames[:, i]

    # Save the result
    denoised_file = f"{os.path.splitext(file)[0]}_denoised.wav"
    sf.write(denoised_file, y_filtered, sr, subtype='PCM_16')

    return denoised_file

def transcribe(audio_path):
    result = model.transcribe(audio_path)
    return " ".join([seg['text'] for seg in result.get('segments', [])])

def process(file):
    # Apply noise suppression and threshold filtering
    denoised_file = noise_reduction(file)

    # Transcribe both original and denoised audio
    # original_text = transcribe(file)
    cleaned_text = transcribe(denoised_file)
    return cleaned_text

    # Print and calculate WER (Word Error Rate)
    # Include param ref for testing
    # print("Original Text:", original_text)
    # print("Denoised Text:", cleaned_text)
    # print(f"Original WER: {wer(ref, original_text) * 100:.2f}%")
    # print(f"Denoised WER: {wer(ref, cleaned_text) * 100:.2f}%")
