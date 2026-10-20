#!/usr/bin/env python3

import datetime
import os
import subprocess
from pathlib import Path

import speech_recognition as sr
from PySide6.QtCore import QThread

# Czas oczekiwania na wypowiedz uzytkownika
WAIT_FOR_INPUT_TIME = 1

class CommandListener(QThread):
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
                        "Nie można zażądać wyników z usługi Google Speech Recognition "
                        "service; {0}".format(error)
                    )
                    continue

                if command == "stop":
                    break

                self.run_makro(command)

        print("Koniec")

    @staticmethod
    def run_makro(command):
        filename = command + ".py"
        print("Próbuję uruchomić plik: " + filename)

        try:
            subprocess.Popen(["python", "makra/" + filename])

            logs_path = Path("./logs")
            logs_path.mkdir(exist_ok=True)

            if len(os.listdir(logs_path)) > 10:
                logs = [log for log in logs_path.iterdir() if log.is_file()]
                oldest_log = min(logs, key=os.path.getmtime)
                oldest_log.unlink()

            now = datetime.datetime.now()
            log_name = f"log_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
            with open(logs_path / log_name, "w", encoding="utf-8") as log:
                log.write(command)
        except FileNotFoundError:
            print("Błąd: Nie znaleziono pliku o nazwie " + filename)
        except subprocess.CalledProcessError:
            print("Błąd: Plik " + filename + " wywołał błąd podczas działania.")


if __name__ == "__main__":
    listener = CommandListener()
    listener.start()
    listener.wait()