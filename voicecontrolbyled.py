import speech_recognition as sr
import RPi.GPIO as GPIO
import tkinter as tk
from threading import Thread

# GPIO Setup
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

# GUI Setup
class LEDApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Smart Home LED Controller")
        self.status_label = tk.Label(root, text="LED Status: OFF", font=("Arial", 20))
        self.status_label.pack(pady=20)
        self.listen_button = tk.Button(root, text="Start Voice Command", command=self.start_listening, font=("Arial", 14))
        self.listen_button.pack(pady=10)

    def update_status(self, status):
        self.status_label.config(text=f"LED Status: {status}")

    def start_listening(self):
        thread = Thread(target=listen_command)
        thread.start()

# Voice Command Processing
def listen_command():
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=2)  # Set to your actual microphone device index

    with mic as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Recognized Command: {command}")
        if "on" in command:
            GPIO.output(LED_PIN, GPIO.HIGH)
            app.update_status("ON")
        elif "off" in command:
            GPIO.output(LED_PIN, GPIO.LOW)
            app.update_status("OFF")
        else:
            print("Command not recognized. Say 'on' or 'off'.")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")

# Start GUI
root = tk.Tk()
app = LEDApp(root)
root.mainloop()

# Cleanup GPIO on exit
GPIO.cleanup()
