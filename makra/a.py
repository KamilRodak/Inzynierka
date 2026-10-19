import pyaudio

# Inicjalizacja PyAudio
p = pyaudio.PyAudio()

try:
    # Pobranie informacji o domyślnym mikrofonie systemowym
    default_info = p.get_default_input_device_info()
    print("--- INFORMACJE O DOMYŚLNYM MIKROFONIE ---")
    print(f"Indeks urządzenia (Device Index): {default_info['index']}")
    print(f"Nazwa urządzenia: {default_info['name']}")
    print(f"Liczba kanałów wejściowych: {default_info['maxInputChannels']}")
except IOError:
    print("Błąd: Nie wykryto żadnego domyślnego urządzenia wejściowego!")

p.terminate()