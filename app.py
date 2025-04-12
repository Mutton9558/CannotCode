import mic_record
import audio_processing
import res
import threading
import time

stop_event = threading.Event()

def audioRecord():
    while not stop_event.is_set():
        mic_record.record_on_voice()  # Blocking
        if stop_event.is_set():
            break
        transcribed_text = audio_processing.process("recorded_voice.wav")
        if stop_event.is_set():
            break
        print(res.generate_response(transcribed_text=transcribed_text))
        time.sleep(1)

def waitUserInput():
    input("Press Enter to stop recording...\n")
    stop_event.set()

# Start threads
recording_thread = threading.Thread(target=audioRecord)
input_thread = threading.Thread(target=waitUserInput)

recording_thread.start()
input_thread.start()

if __name__ == "__main__":
    recording_thread.join()
    input_thread.join()
