import speech_recognition as sr
import time
import keyboard

recognizer = sr.Recognizer()
microphone = sr.Microphone()

AUDIO_TIMEOUT = 10  
PHRASE_TIME_LIMIT = 20
ENERGY_THRESHOLD = 400  # minimum audio energy to consider for recording
PAUSE_THRESHOLD = 2  # seconds of non-speaking audio before a phrase is considered complete
PHRASE_TIME_LIMIT = 20  # the maximum number of seconds that it will allow a phrase to continue before stopping and returning the part of the phrase processed before the time limit was reached. If None, no time limit is enforced.

recognizer = sr.Recognizer()
microphone = sr.Microphone()
recognizer.pause_threshold = PAUSE_THRESHOLD
recognizer.energy_threshold = ENERGY_THRESHOLD
transcription_file = "lecture_notes.txt"

# Adjust for ambient noise initially
with microphone as source:
    print("Adjusting for ambient noise...", end=" ")
    recognizer.adjust_for_ambient_noise(source, duration=2)
    print("Mic energy threshold set at", int(recognizer.energy_threshold))
    
def continuous_transcription_callback(recognizer, audio):
    try:
        transcription = recognizer.recognize_whisper(audio, model="base.en", language=None)
        print("Teacher: ", transcription)    
        
        with open(transcription_file, "a") as file:
            file.write(transcription, end="\n")    
        
    except sr.UnknownValueError:
        print("Whisper could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Whisper service; {e}")
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase to start")
    except Exception as e:
        print(f"Unknown exception occurred: {e}")
# Start the background listening
stop_listening = recognizer.listen_in_background(microphone, continuous_transcription_callback, phrase_time_limit=PHRASE_TIME_LIMIT)

try:
    while True:
        time.sleep(0.1)
        if keyboard.is_pressed('esc'):
            break
except KeyboardInterrupt:
    print("Exiting...")
