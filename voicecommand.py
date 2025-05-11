import speech_recognition as sr
from gpiozero import LED
from tkinter import *
import threading

# Setup LED
led = LED(17)

# Setup GUI
window = Tk()
window.title("LED Voice Control")
window.geometry("320x180")
status_label = Label(window, text="LED Status: OFF", font=("Arial", 16))
status_label.pack(pady=10)

feedback_label = Label(window, text="", font=("Arial", 12), fg="blue")
feedback_label.pack(pady=5)

def update_status(state):
    status_label.config(text=f"LED Status: {'ON' if state else 'OFF'}")

def update_feedback(text, color="blue"):
    feedback_label.config(text=text, fg=color)

def listen_command():
    recognizer = sr.Recognizer()
    try:
        mic = sr.Microphone(device_index=2)
    except OSError as e:
        update_feedback(f"Microphone error: {e}", "red")
        speak_button.config(state=NORMAL)
        return

    with mic as source:
        update_feedback("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            update_feedback("Listening timed out.", "red")
            speak_button.config(state=NORMAL)
            return

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)

        if "on" in command:
            led.on()
            update_status(True)
            update_feedback("LED turned ON.")
        elif "off" in command:
            led.off()
            update_status(False)
            update_feedback("LED turned OFF.")
        else:
            update_feedback("Command not recognized.", "red")

    except sr.UnknownValueError:
        update_feedback("Could not understand audio.", "red")
    except sr.RequestError as e:
        update_feedback(f"API error: {e}", "red")

    speak_button.config(state=NORMAL)

def threaded_listen():
    speak_button.config(state=DISABLED)
    threading.Thread(target=listen_command).start()

speak_button = Button(window, text="Speak", command=threaded_listen, font=("Arial", 14))
speak_button.pack(pady=10)

window.mainloop()
