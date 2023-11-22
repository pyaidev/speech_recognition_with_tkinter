import tkinter as tk
from tkinter import scrolledtext
import threading
import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

class SpeechRecognitionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Speech Recognition App")

        # Create GUI elements
        self.label = tk.Label(master, text="Microphone List:")
        self.label.pack()

        self.listbox = tk.Listbox(master)
        self.listbox.pack()

        self.button = tk.Button(master, text="Start Speech Recognition", command=self.start_recognition)
        self.button.pack()

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=40, height=10)
        self.text_area.pack()

    def start_recognition(self):
        # Get the selected microphone index from the listbox
        selected_mic_index = self.listbox.curselection()[0]

        # Use the selected microphone as the audio source
        mic = sr.Microphone(device_index=selected_mic_index)

        # Adjust for ambient noise
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)

        # Function to listen to the microphone and update the text area
        def listen_to_microphone():
            with mic as source:
                self.text_area.insert(tk.END, "Listening...\n")
                audio = recognizer.listen(source)

            try:
                self.text_area.insert(tk.END, "Recognizing...\n")
                # Using Google Web Speech API for recognition
                text = recognizer.recognize_google(audio, language="ru_RU")
                self.text_area.insert(tk.END, f"Text: {text}\n")
            except sr.UnknownValueError:
                self.text_area.insert(tk.END, "Speech Recognition could not understand audio\n")
            except sr.RequestError as e:
                self.text_area.insert(tk.END, f"Could not request results from Google Web Speech API; {e}\n")
        thread = threading.Thread(target=listen_to_microphone)
        thread.start()

def main():
    root = tk.Tk()
    app = SpeechRecognitionApp(root)
    list_mic = sr.Microphone.list_microphone_names()
    for mic_name in list_mic:
        app.listbox.insert(tk.END, mic_name)
    root.mainloop()

if __name__ == "__main__":
    main()
