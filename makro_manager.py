import datetime
import os
import subprocess
import sys
from config import MAKRA_PATH, LOGS_PATH


class MacroManager:
    @staticmethod
    def run_script(macro_name, original_command):
        file_path = MAKRA_PATH / f"{macro_name}.py"
        print(f"Próbuję uruchomić: {file_path}")

        try:
            subprocess.Popen([sys.executable, str(file_path)])
            MacroManager._log_execution(file_path, original_command)
        except FileNotFoundError:
            print(f"Nie znaleziono pliku: {file_path}.")
        except Exception as e:
            print(f"Błąd wykonania skryptu: {e}")

    @staticmethod
    def _log_execution(file_path, original_command):
        if len(os.listdir(LOGS_PATH)) > 10:
            logs = [log for log in LOGS_PATH.iterdir() if log.is_file()]
            if logs:
                min(logs, key=os.path.getmtime).unlink()

        now = datetime.datetime.now()
        log_file = LOGS_PATH / f"log_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        with open(log_file, "w", encoding="utf-8") as log:
            log.write(f"Komenda: {original_command}\nSkrypt: {file_path}")