from PIL import Image
from customtkinter import *
from prefs import preferences
import os
import threading
import qrcode
from misc import format_file_size


class Upload(CTkFrame):
    def __init__(self, master, upload_func: callable):

        super().__init__(master=master, fg_color=preferences["BACKGROUND_COLOR"])

        self.file_path = None

        # Add the passed through functions for later use
        self.upload_func = upload_func

        self.create_widgets()
        self.password_field.configure(state="disabled")

    def create_widgets(self):

        # Create the progress variables which self update GUI elements whenever they change
        self.progress = DoubleVar()
        self.progress.trace("w", self.update_progress_string)
        self.progress_string = StringVar()

        # Create the pick file button
        self.pick_file_button = CTkButton(self, text="Pick file", command=self.pick_file)

        # Create the file selection widgets
        self.file_frame = CTkFrame(self, fg_color=preferences["BACKGROUND_COLOR"])
        self.file_icon = CTkLabel(self.file_frame, text='')
        self.file_label = CTkLabel(self.file_frame, text="No file selected")
        self.size_label = CTkLabel(self, text="")

        # Create the password protection widgets
        self.password_checkbox = CTkCheckBox(self,
                                             text='Password protected',
                                             checkbox_width=15,
                                             checkbox_height=15,
                                             border_width=1,
                                             command=self.toggle_password)
        self.password_field = CTkEntry(self, placeholder_text="Password")

        # Create the progress bar widgets
        self.bar_label = CTkLabel(self, text="Progress:")
        self.progress_frame = CTkFrame(self, fg_color=preferences["BACKGROUND_COLOR"])
        self.progress_bar = CTkProgressBar(self.progress_frame, variable=self.progress)
        self.progress_label = CTkLabel(self.progress_frame, textvariable=self.progress_string)

        # Create the upload button
        self.upload_file_button = CTkButton(self, text="Upload", command=self.upload_file, state="disabled")

        # Layout using pack
        self.pick_file_button.pack(pady=10)

        self.file_icon.pack(side="left", pady=5)
        self.file_label.pack(side="left", pady=0)
        self.file_frame.pack(pady=0)
        self.size_label.pack(pady=0)

        self.password_checkbox.pack(pady=5)
        self.password_field.pack(pady=0)

        self.upload_file_button.pack(pady=10)

        self.bar_label.pack(pady=0)
        self.progress_bar.pack(side="left", padx=10)
        self.progress_label.pack(side="left", padx=10)
        self.progress_frame.pack(pady=0)

    def pick_file(self):
        """
        Method for picking a file from the file system using a file explorer dialog
        :return:
        """
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        # Update the file selection widgets with the newly selected file
        self.file_path = file_path
        self.file_label.configure(text=os.path.basename(file_path))
        self.file_icon.configure(image=CTkImage(Image.open("./assets/file.webp"), size=(20, 20)))
        self.size_label.configure(text=f"Size: {format_file_size(os.path.getsize(file_path))}")
        self.upload_file_button.configure(state="normal")

    def clear_selection(self):
        """
        Method for clearing the file selection and resetting the GUI elements after a successful upload
        :return:
        """
        self.file_path = None
        self.file_label.configure(text="No file selected")
        self.file_icon.configure(image=None)
        self.size_label.configure(text="")
        self.upload_file_button.configure(state="disabled")
        self.progress.set(0)
        self.password_checkbox.deselect()
        self.password_field.delete(0, len(self.password_field.get()))
        self.password_field.configure(state="disabled")

    def upload_file(self):
        password = None
        if self.password_checkbox.get():
            password = self.password_field.get()

        # Start a new thread to upload the file in order for the progress bar to update in real time
        threading.Thread(target=self.upload_func, args=(self.file_path, self.progress, password)).start()

    def update_progress_string(self, *args):
        # Update the progress string with the current progress, capped at 100%
        percentage = round(self.progress.get() * 100) if self.progress.get() < 1 else 100
        self.progress_string.set(f"{percentage}%")

    def toggle_password(self):
        """
        Method for enabling or disabling the password field based on the state of the password checkbox
        :return:
        """
        if self.password_checkbox.get():
            self.password_field.configure(state="normal")
        else:
            # Clear and disable the password field
            self.password_field.delete(0, len(self.password_field.get()))
            self.password_field.configure(state="disabled")


class PostUpload(CTkToplevel):
    def __init__(self, master, url, close_func: callable):
        super().__init__(master=master, fg_color=preferences["BACKGROUND_COLOR"])

        # Set the window properties
        self.title("Upload successful!")
        self.geometry("600x350")

        # Add the passed through functions for later use
        self.close_func = close_func

        self.create_widgets(url)

    def create_widgets(self, url):

        # Create the label, qr image, and button
        self.label = CTkLabel(self, text="Upload successful!")
        self.url_label = CTkLabel(self, text=url)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        img.save("qrcode.png")

        self.qr_code_image = CTkImage(Image.open("qrcode.png"), size=(200, 200))
        self.qr_code_label = CTkLabel(self, image=self.qr_code_image, text='')

        self.copy_button = CTkButton(self, text="Copy URL",
                                     image=CTkImage(Image.open("./assets/copy.webp")),
                                     command=self.copy_url)

        # Vertical layout using pack
        self.label.pack()
        self.url_label.pack()
        self.qr_code_label.pack(pady=10)
        self.copy_button.pack(pady=5)

    def copy_url(self):
        self.clipboard_clear()
        self.clipboard_append(self.url_label.cget("text"))
        self.update()

    def destroy(self):
        self.close_func()
        super().destroy()

