from PIL import Image
from customtkinter import *
from CTkListbox import *


class MyFiles(CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, width=650, height=300)
        self.create_widgets()

    def create_widgets(self):

        self.btn_frame = CTkFrame(self)
        # Create the buttons
        self.download_button = CTkButton(self.btn_frame, text="Download",
                                         image=CTkImage(Image.open("./assets/upload.webp").rotate(180)),
                                         command=self.download_file)
        self.download_button.grid(row=0, column=0, padx=10, pady=10)

        self.share_button = CTkButton(self.btn_frame, text="Share",
                                      image=CTkImage(Image.open("./assets/shared_files.webp")),
                                      command=self.share_file)
        self.share_button.grid(row=1, column=0, padx=10, pady=10)

        self.private_button = CTkButton(self.btn_frame, text="Make Private",
                                        command=self.make_private)
        self.private_button.grid(row=2, column=0, padx=10, pady=10)

        self.delete_button = CTkButton(self.btn_frame, text="Delete",
                                       image=CTkImage(Image.open("./assets/delete.webp")),
                                       command=self.delete_file)
        self.delete_button.grid(row=3, column=0, padx=10, pady=10)

        self.btn_frame.pack(side="left", fill="y", pady=100)

        self.file_list = CTkListbox(self)
        self.file_list.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def download_file(self):
        pass

    def share_file(self):
        dialog = ShareDialog(self)
        dialog.grab_set()

    def make_private(self):
        pass

    def delete_file(self):
        pass


class ShareDialog(CTkToplevel):
    def __init__(self, master):
        super().__init__(master=master)
        self.create_widgets()

    def create_widgets(self):
        self.label = CTkLabel(self, text="Share with (enter username):")
        self.label.pack()

        self.entry = CTkEntry(self)
        self.entry.pack()

        self.share_button = CTkButton(self, text="Share", command=self.share)
        self.share_button.pack()

    def share(self):
        pass
