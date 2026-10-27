#!/usr/bin/env python3

from config import WAIT_FOR_INPUT_TIME
import speech_recognition as sr
from PySide6.QtCore import QThread
from ai_router import AIRouter

class CommandListener(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ai_router = AIRouter()

    def run(self):
        recognizer = sr.Recognizer()
        recognizer.phrase_threshold = 0.5
        recognizer.pause_threshold = 0.5
        microphone = sr.Microphone()

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)

            print("Słucham")

            while True:
                try:
                    audio = recognizer.listen(source, timeout=WAIT_FOR_INPUT_TIME)
                except sr.WaitTimeoutError:
                    continue

                try:
                    command = recognizer.recognize_google(
                        audio,
                        language="pl-PL",
                    )
                    print("Google Speech Recognition rozpoznało: " + command)
                except sr.UnknownValueError:
                    print("Google Speech Recognition nie rozpoznało audio")
                    continue
                except sr.RequestError as error:
                    print(
                        "Nie można pobrać wyników z usługi Google Speech Recognition "
                        "service; {0}".format(error)
                    )
                    continue

                if command == "stop":
                    break

                self.ai_router.route_command(command)

        print("Koniec")