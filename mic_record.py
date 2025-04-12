import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

THRESHOLD = 0.05
SILENCE_DURATION = 2.0
SAMPLE_RATE = 16000
FRAME_DURATION = 0.1
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION)
OUTPUT_FILENAME = "recorded_voice.wav"

def record_on_voice():
    print("🎤 Waiting for speech...")

    recording = []
    silence_time = 0.0
    speaking = False

    def audio_callback(indata, frames, time_info, status):
        nonlocal recording, silence_time, speaking

        volume = np.linalg.norm(indata)
        is_voice = volume > THRESHOLD

        if is_voice:
            if not speaking:
                print("🗣️ Voice detected. Recording...")
                speaking = True
            silence_time = 0.0
            recording.append(indata.copy())
        elif speaking:
            silence_time += FRAME_DURATION
            recording.append(indata.copy())
            if silence_time > SILENCE_DURATION:
                print("🔇 Silence detected. Stopping recording.")
                raise sd.CallbackStop()

    with sd.InputStream(callback=audio_callback,
                        channels=1,
                        samplerate=SAMPLE_RATE,
                        blocksize=FRAME_SIZE):
        sd.sleep(10000)  # Wait until callback stops (10s max safety)

    if recording:
        audio_data = np.concatenate(recording, axis=0)
        audio_int16 = np.int16(audio_data * 32767)
        wav.write(OUTPUT_FILENAME, SAMPLE_RATE, audio_int16)
        print(f"✅ Saved recording to: {OUTPUT_FILENAME}")
    else:
        print("⚠️ No voice detected.")

record_on_voice()