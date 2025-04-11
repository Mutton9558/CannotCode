import mic_record
import audio_processing

if __name__ == "__main__":
    while True:
        mic_record.record_on_voice()
        audio_processing.process("recorded_voice.wav")
