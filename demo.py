#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import time
import subprocess
import speech_recognition as sr

last_audio=""
new_command_available = False
# this is called from the background thread
def callback(recognizer, audio):
    global last_audio
    global new_command_available
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        last_audio=recognizer.recognize_google(audio,language="pl-PL")
        
        print("Google Speech Recognition thinks you said " + last_audio)
        new_command_available = True
        
        
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        new_command_available = False
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


r = sr.Recognizer()
r.phrase_threshold = 0.5
r.pause_threshold = 0.6
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
print("słucham")
# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

while last_audio!="stop":
    if new_command_available and last_audio != "stop" and last_audio!="":
        nazwa_pliku = last_audio + ".py"
        print("Próbuję uruchomić plik: "+nazwa_pliku)
        try:
            subprocess.Popen(["python","makra/"+last_audio+".py" ])
        except FileNotFoundError:
            print("Błąd: Nie znaleziono pliku o nazwie "+ nazwa_pliku)
        except subprocess.CalledProcessError:
            print("Błąd: Plik "+nazwa_pliku+" wywołał błąd podczas działania.")
        new_command_available = False
    time.sleep(0.1)        
# calling this function requests that the background listener stop listening

stop_listening(wait_for_stop=False)
print("done")
            
