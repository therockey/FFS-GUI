from PIL import Image
from customtkinter import *
from CTkListbox import *


class SharedFiles(CTkFrame):
    def __init__(self, master,
                 files: list[dict],
                 download_file: callable):
        super().__init__(master=master)

        self.files = files
        self.download_file = download_file

        self.create_widgets()

    def create_widgets(self):
        self.btn_frame = CTkFrame(self)

        self.filename = CTkLabel(self.btn_frame, text="Filename: ")
        self.filename.grid(row=0, column=0, padx=10, pady=10)

        self.sizelabel = CTkLabel(self.btn_frame, text="Size: ")
        self.sizelabel.grid(row=1, column=0, padx=10, pady=10)

        self.owner = CTkLabel(self.btn_frame, text="Owner: ")
        self.owner.grid(row=2, column=0, padx=10, pady=10)

        self.download_button = CTkButton(self.btn_frame, text="Download",
                                         image=CTkImage(Image.open("./assets/upload.webp").rotate(180)),
                                         command=self.download)

        self.download_button.grid(row=3, column=0, padx=10, pady=10)

        self.btn_frame.pack(side="left", fill="y", pady=100)

        self.file_list = CTkListbox(self, multiple_selection=False)
        self.file_list.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def get_selected_file(self) -> str | None:
        selection = self.file_list.get()
        if selection:
            return self.files[selection]['file_token']

        return None

    def download(self):
        file_token = self.get_selected_file()
        if file_token:
            self.download_file(file_token)

    def update_file_info(self):
        file = self.files[self.file_list.get()]


