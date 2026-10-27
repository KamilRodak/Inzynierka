#!/usr/bin/env python3

from voice_recognition import CommandListener
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    listener = CommandListener()
    listener.start()
    listener.wait()