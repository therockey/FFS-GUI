from customtkinter import *
from prefs import preferences
from tkinter import filedialog, DoubleVar
import file_ops
import os
import threading


class Upload(CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.configure(fg_color=preferences["BACKGROUND_COLOR"])
        self.create_widgets()

    def create_widgets(self):
        self.progress = DoubleVar()
        self.progress.trace("w", self.update_progress_string)
        self.progress_string = StringVar()

        self.pick_file_button = CTkButton(self, text="Pick file", command=self.pick_file)
        self.file_label = CTkLabel(self, text="No file selected")

        self.progress_frame = CTkFrame(self, fg_color=preferences["BACKGROUND_COLOR"])
        self.progress_bar = CTkProgressBar(self.progress_frame, variable=self.progress)
        self.progress_label = CTkLabel(self.progress_frame, textvariable=self.progress_string)

        self.upload_file_button = CTkButton(self, text="Upload", command=lambda: self.upload_file(self.file_path), state="disabled")




        self.pick_file_button.pack(pady=10)
        self.file_label.pack(pady=10)
        self.upload_file_button.pack(pady=10)


        self.progress_bar.pack(side="left", pady=10)
        self.progress_label.pack(side="left", pady=20)
        self.progress_frame.pack(pady=10)


    def pick_file(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.file_path = file_path
        self.file_label.configure(text=os.path.basename(file_path))
        self.upload_file_button.configure(state="normal")

    def upload_file(self, file_path):
        threading.Thread(target=file_ops.upload_file, args=(file_path, self.progress)).start()

    def update_progress_string(self, *args):
        self.progress_string.set(f"{round(self.progress.get()*100)}%")
