from PIL import Image
from customtkinter import *
from CTkListbox import *


class MyFiles(CTkFrame):
    def __init__(self, master,
                 files: list[dict],
                 download_file: callable,
                 share_file: callable,
                 make_private: callable,
                 delete_file: callable):

        super().__init__(master=master, width=650, height=300)

        self.files = files
        self.download_file = download_file
        self.share_file = share_file
        self.make_private = make_private
        self.delete_file = delete_file

        self.create_widgets()

    def create_widgets(self):

        self.btn_frame = CTkFrame(self)
        # Create the buttons
        self.download_button = CTkButton(self.btn_frame, text="Download",
                                         image=CTkImage(Image.open("./assets/upload.webp").rotate(180)),
                                         command=self.download)
        self.download_button.grid(row=0, column=0, padx=10, pady=10)

        self.share_button = CTkButton(self.btn_frame, text="Share",
                                      image=CTkImage(Image.open("./assets/shared_files.webp")),
                                      command=self.share)
        self.share_button.grid(row=1, column=0, padx=10, pady=10)

        self.private_button = CTkButton(self.btn_frame, text="Make Private",
                                        command=self.private)
        self.private_button.grid(row=2, column=0, padx=10, pady=10)

        self.delete_button = CTkButton(self.btn_frame, text="Delete",
                                       image=CTkImage(Image.open("./assets/delete.webp")),
                                       command=self.delete)
        self.delete_button.grid(row=3, column=0, padx=10, pady=10)

        self.btn_frame.pack(side="left", fill="y", pady=100)

        self.file_list = CTkListbox(self, multiple_selection=False)
        self.file_list.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def display_files(self, files: list[dict]):
        for file in files:
            self.file_list.insert("END", file['filename'])

    def get_selected_file(self) -> str | None:
        selection = self.file_list.get()
        if selection:
            return self.files[selection]['file_token']

        return None

    def download(self):
        file_token = self.get_selected_file()
        if file_token:
            self.download_file(file_token)

    def share(self):
        file_token = self.get_selected_file()
        if file_token:
            dialog = ShareDialog(self, self.share_file, file_token)
            dialog.grab_set()

    def private(self):
        file_token = self.get_selected_file()
        if file_token:
            self.make_private(file_token)

    def delete(self):
        file_token = self.get_selected_file()
        if file_token:
            self.delete_file(file_token)


class ShareDialog(CTkToplevel):
    def __init__(self, master, share_func: callable, file_token: str):
        super().__init__(master=master)
        self.share_func = share_func
        self.file_token = file_token
        self.create_widgets()

    def create_widgets(self):
        self.label = CTkLabel(self, text="Share with (enter username):")
        self.label.pack()

        self.entry = CTkEntry(self)
        self.entry.pack()

        self.share_button = CTkButton(self, text="Share", command=self.share)
        self.share_button.pack()

    def share(self):
        username = self.entry.get()
        self.share_func(self.file_token, username)
        self.destroy()
