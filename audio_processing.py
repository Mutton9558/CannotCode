import noisereduce as nr
import librosa
from jiwer import wer
import soundfile as sf
import os
import whisperx

# Load WhisperX model
device = "cpu"
model = whisperx.load_model("base", device=device, compute_type="float32")

def fast_noise_reduction(file):
    # Load audio in mono, 16kHz (same as model expectation)
    y, sr = librosa.load(file, sr=16000, mono=True)

    # Fast noise reduction
    reduced = nr.reduce_noise(y=y, sr=sr, prop_decrease=0.7)

    # Save to new file
    denoised_file = f"{os.path.splitext(file)[0]}_denoised.wav"
    sf.write(denoised_file, reduced, sr, subtype='PCM_16')

    return denoised_file

def transcribe(audio_path):
    result = model.transcribe(audio_path, language="en")
    return " ".join([seg['text'] for seg in result.get('segments', [])])

def test(file, ref):
    denoised_file = fast_noise_reduction(file)

    original_text = transcribe(file)
    cleaned_text = transcribe(denoised_file)

    print("Original Text:", original_text)
    print("Denoised Text:", cleaned_text)
    print(f"Original WER: {wer(ref, original_text) * 100:.2f}%")
    print(f"Denoised WER: {wer(ref, cleaned_text) * 100:.2f}%")

test("test1.wav", "Show me summary of my last five rides.")
