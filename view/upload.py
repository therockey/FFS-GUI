from PIL import Image
from customtkinter import *
from prefs import preferences
import os
import threading
import qrcode
from PIL import ImageTk


class Upload(CTkFrame):
    def __init__(self, master, upload_func: callable):
        super().__init__(master=master)
        self.configure(fg_color=preferences["BACKGROUND_COLOR"])
        self.file_path = None
        self.upload_func = upload_func
        self.create_widgets()

    def create_widgets(self):
        self.progress = DoubleVar()
        self.progress.trace("w", self.update_progress_string)
        self.progress_string = StringVar()

        self.pick_file_button = CTkButton(self, text="Pick file", command=self.pick_file)

        self.file_frame = CTkFrame(self, fg_color=preferences["BACKGROUND_COLOR"])
        self.file_icon = CTkLabel(self.file_frame, text='')
        self.file_label = CTkLabel(self.file_frame, text="No file selected")

        self.size_label = CTkLabel(self, text="")

        self.bar_label = CTkLabel(self, text="Progress:")
        self.progress_frame = CTkFrame(self, fg_color=preferences["BACKGROUND_COLOR"])
        self.progress_bar = CTkProgressBar(self.progress_frame, variable=self.progress)
        self.progress_label = CTkLabel(self.progress_frame, textvariable=self.progress_string)

        self.upload_file_button = CTkButton(self, text="Upload", command=self.upload_file, state="disabled")

        self.pick_file_button.pack(pady=10)

        self.file_icon.pack(side="left", pady=5)
        self.file_label.pack(side="left", pady=0)
        self.file_frame.pack(pady=0)

        self.size_label.pack(pady=0)
        self.upload_file_button.pack(pady=10)

        self.bar_label.pack(pady=0)
        self.progress_bar.pack(side="left", padx=10)
        self.progress_label.pack(side="left", padx=10)
        self.progress_frame.pack(pady=0)

    def pick_file(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.file_path = file_path
        self.file_label.configure(text=os.path.basename(file_path))
        self.file_icon.configure(image=CTkImage(Image.open("./assets/file.webp"), size=(20, 20)))
        self.size_label.configure(text=f"Size: {round(os.path.getsize(file_path) / 1024 / 1024, 2)} MB")
        self.upload_file_button.configure(state="normal")

    def upload_file(self):
        threading.Thread(target=self.upload_func, args=(self.file_path, self.progress)).start()

    def update_progress_string(self, *args):
        self.progress_string.set(f"{round(self.progress.get() * 100)}%")


class PostUpload(CTkToplevel):
    def __init__(self, master, url):
        super().__init__(master=master)
        self.create_widgets(url)

    def create_widgets(self, url):
        self.label = CTkLabel(self, text="Upload successful!")
        self.label.pack()

        self.url_label = CTkLabel(self, text=url)
        self.url_label.pack()

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        self.qr_code_image = ImageTk.PhotoImage(img)

        self.qr_code_label = CTkLabel(self, image=self.qr_code_image)
        self.qr_code_label.pack()

        self.copy_button = CTkButton(self, text="Copy URL", command=self.copy_url)
        self.copy_button.pack()

    def copy_url(self):
        self.clipboard_clear()
        self.clipboard_append(self.url_label.cget("text"))
        self.update()
