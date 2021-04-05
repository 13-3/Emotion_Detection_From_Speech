
from tkinter import *

from tkinter import ttk

import mysql.connector

import os as os
import librosa
import math
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow.keras as keras
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, AveragePooling1D
from keras.layers import Dense, Embedding
from tensorflow.keras import optimizers
from keras.layers import Input, Flatten, Dropout, Activation
import time
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

import librosa.display

from sklearn.metrics import accuracy_score , confusion_matrix

import pyaudio
import wave




mydb = mysql.connector.connect(host="192.168.100.88", user="root", password="", database="EmotionDetection")

mycor = mydb.cursor()

# quary = "INSERT INTO student (stID,fName,lName,age) VALUES (1111111111, \"aaa\", \"Alshehri\", \"12\")"


# mydb.commit()
# rint(mycor.rowcount, "record inserted.")


# splash screen 4 logo
splash_root = Tk()
splash_root.title("Splash Screen!")
splash_root.geometry("280x120")
splash_root.overrideredirect(True)
logo_splash = PhotoImage(file="EmotionDetectionLogo.png")
splash_lbl = Label(splash_root, image=logo_splash)
splash_lbl.pack()
mydb.commit()

def record():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "venv/audio/output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()





#  Initialize main window
def main_window():
    splash_root.destroy()
    root = Tk()
    # window name
    root.title("Emotion Detection")
    # window size
    root.geometry("480x320")
    # Create Frames to organize layouts
    # Top Frame
    top_frame = Frame(root)
    top_frame.pack()
    top_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    # add label txt

    childID_lbl = Label(top_frame, text="Child ID: ", justify=CENTER, font=("Calibre", 14, "italic", UNDERLINE), fg="#87AFC7")
    childID_lbl.pack(side=TOP, padx=10)
    # variable for stor student id
    q = IntVar()
    # add textbox
    # textvariable=q for stoe id to using it in view windowS
    childID_entry = Entry(top_frame, textvariable=q, width=20)
    childID_entry.pack(pady=10, side=TOP)

    # onclick access -> open new window
    def access_win():
        root1 = Tk()
        root1.title("Home")
        root1.geometry("480x320")

        # Top Frame to centralized buttons
        top_frame2 = Frame(root1)
        top_frame2.pack(side=TOP)
        top_frame2.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Left Frame for arrow
        left_frame = Frame(root1)
        left_frame.pack(side=LEFT)
        left_frame.place(relx=0.05, rely=0.08, anchor=N)

        def stop_win():
            root3 = Tk()
            root3.title("Detected Emotions")
            root3.geometry("480x320")
            detected_emotion_lbl = Label(root3, text="The Detected Emotion is: ",
                                         font=("Calibra", 14, "italic", UNDERLINE), justify=CENTER, fg="#87AFC7")
            detected_emotion_lbl.pack(side=LEFT, padx=80)

        # Start Button
        start_btn = Button(top_frame2, text="Start Recording", bg="#87AFC7", fg="white", borderwidth=2)
        start_btn.pack(side=LEFT, padx=10, pady=10)

        # Stop Button
        stop_btn = Button(top_frame2, text="Stop Recording", bg="#87AFC7", fg="white", borderwidth=2, onClick=record(),command=stop_win)
        stop_btn.pack(side=LEFT, padx=10, pady=10)

    # end of stop window

    # end of access window

    # onclick view -> open new window to view child emotions
    def update(rows, tv):
        for x in rows:
            tv.insert('', 'end', values=x)

    def view_win():
        root5 = Tk()
        root5.title("View")
        root5.geometry("480x320")
        wrapear = LabelFrame(root5, text="Student data")
        wrapear.pack(fill="both", expand="yes", padx=20, pady=10)
        tv = ttk.Treeview(wrapear, columns=(1, 2, 3, 4), show="headings", heigh="6")
        tv.pack()
        tv.heading(1, text="ID")
        tv.heading(2, text="First name")
        tv.heading(3, text="Last name")
        tv.heading(4, text="Emotion")

        # mycor.execute("Select * from Child where childID=%s "%(q.get()))
        mycor.execute("Select Child.childID , Child.firstName , Child.lastName , Emotion.emotionName from Child inner join Emotion on Child.emotionID = Emotion.emotionID where Child.childID =%s "%(q.get()))
        rows = mycor.fetchall()
        update(rows, tv)

    # View Button
    view_btn = Button(top_frame, text="  View   ", bg="#87AFC7", fg="white", borderwidth=2, command=view_win)
    view_btn.pack(side=LEFT, padx=10, pady=10)
    # Access Button
    access_btn = Button(top_frame, text=" Access ", bg="#87AFC7", fg="white", borderwidth=2, command=access_win)
    access_btn.pack(side=RIGHT, padx=10, pady=10)

    # end of view window


# end of main window function
# splash screen timer
splash_root.after(3000, main_window)
mainloop()


if __name__=="__main__":
    print("hello")
