import os
from groq import Groq
from RealtimeSTT import AudioToTextRecorder
import pyttsx3
from pynput import keyboard
import threading
import time
import tkinter as tk
from PIL import Image, ImageTk, ImageOps  # You need Pillow for this


recordingnow = False  # Global flag to track recording status








# Function to record and transcribe while F7 is held
def get_transcribed_text():
    global recordingnow
    recorder = AudioToTextRecorder()

    print("Hold F7 to start talking...")
    while True:
        if recordingnow:
            print("Recording... speak now.")
            text = recorder.text()
            if text:
                print(f"You said: {text}")
                return text
            time.sleep(0.1)
        else:
            time.sleep(0.1)


# F7 key listener handlers
def on_press(key):
    global recordingnow
    if key == keyboard.Key.f7:
        recordingnow = True

def on_release(key):
    global recordingnow
    if key == keyboard.Key.f7:
        recordingnow = False


# Global conversation history (starts empty or with system prompt)
conversation_history = [
    {"role": "system", "content": "be helpful"}
]

def get_ai_response(text):
    global conversation_history

    client = Groq(api_key="Your Groq API Key")

    # Add user message to conversation
    conversation_history.append({"role": "user", "content": text})

    chat_completion = client.chat.completions.create(
        messages=conversation_history,
        model="llama-3.3-70b-versatile",
    )

    response = chat_completion.choices[0].message.content
    print(f"Chat-bot says: {response}")

    # Add AI response to conversation history
    conversation_history.append({"role": "assistant", "content": response})


    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(response)
    engine.runAndWait()



# Start keyboard listener in background thread
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()


# Main loop
if __name__ == '__main__':
    while True:
        user_text = get_transcribed_text()
        if user_text:
            get_ai_response(user_text)
