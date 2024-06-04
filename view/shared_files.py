from PIL import Image
from customtkinter import *
from CTkListbox import *
from misc import format_file_size
from prefs import preferences


class SharedFiles(CTkFrame):
    def __init__(self, master,
                 get_files: callable,
                 download_file: callable):

        super().__init__(master=master, fg_color=preferences["BACKGROUND_COLOR"])

        self.files = []
        self.get_files = get_files
        self.download_file = download_file

        self.create_widgets()
        self.display_files()

    def create_widgets(self):
        self.btn_frame = CTkFrame(self, fg_color=preferences["BACKGROUND_COLOR"])

        self.filename = CTkLabel(self.btn_frame, text="Filename: ", wraplength=130)
        self.filename.grid(row=0, column=0, padx=10, pady=5)

        self.sizelabel = CTkLabel(self.btn_frame, text="Size: ")
        self.sizelabel.grid(row=1, column=0, padx=10, pady=5)

        self.owner = CTkLabel(self.btn_frame, text="Owner: ")
        self.owner.grid(row=2, column=0, padx=10, pady=5)

        self.download_button = CTkButton(self.btn_frame, text="Download",
                                         image=CTkImage(Image.open("./assets/upload.webp").rotate(180)),
                                         command=self.download)

        self.download_button.grid(row=3, column=0, padx=10, pady=10)

        self.btn_frame.pack(side="left", fill="y", pady=100)

        self.file_list = CTkListbox(self, multiple_selection=False,
                                    command=lambda e: self.update_file_info())
        self.file_list.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def display_files(self):
        self.file_list.insert(0, "")
        self.file_list.delete("all")
        self.files = self.get_files()
        for file in self.files:
            self.file_list.insert("END", file['filename'])

    def get_selected_file(self) -> str | None:
        selection = self.file_list.get()
        for file in self.files:
            if file['filename'] == selection:
                return file['file_token']

        return None

    def download(self):
        file_token = self.get_selected_file()
        if file_token:
            self.download_file(file_token)

    def update_file_info(self):
        file = None
        selection = self.file_list.get()
        for f in self.files:
            if f['filename'] == selection:
                file = f
                break

        self.filename.configure(text=f"Filename: {file['filename']}")
        self.owner.configure(text=f"Owner: {file['owner']}")
        self.sizelabel.configure(text=f"Size: {format_file_size(file['file_size'])}")

