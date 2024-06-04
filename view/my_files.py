from PIL import Image
from customtkinter import *
from CTkListbox import *

from prefs import preferences


class MyFiles(CTkFrame):
    def __init__(self, master,
                 get_files: callable,
                 download_file: callable,
                 share_file: callable,
                 make_private: callable,
                 trash_file: callable):

        super().__init__(master=master,
                         width=650, height=300,
                         fg_color=preferences["BACKGROUND_COLOR"])

        self.files = []

        # Add the passed through functions for later use
        self.get_files = get_files
        self.download_file = download_file
        self.share_file = share_file
        self.make_private = make_private
        self.trash_file = trash_file

        self.create_widgets()
        self.display_files()

    def create_widgets(self):

        # Create the frame to hold the buttons beside the file list
        self.btn_frame = CTkFrame(self, fg_color=preferences["BACKGROUND_COLOR"])

        # Create the buttons
        self.download_button = CTkButton(self.btn_frame, text="Download",
                                         image=CTkImage(Image.open("./assets/upload.webp").rotate(180)),
                                         command=self.download)

        self.share_button = CTkButton(self.btn_frame, text="Share",
                                      image=CTkImage(Image.open("./assets/shared_files.webp")),
                                      command=self.share)

        self.private_button = CTkButton(self.btn_frame, text="Make Private",
                                        command=self.private)

        self.trash_button = CTkButton(self.btn_frame, text="Trash",
                                      image=CTkImage(Image.open("./assets/trash.webp")),
                                      command=self.trash)

        # Create the file list
        self.file_list = CTkListbox(self, multiple_selection=False, )

        # Layout using pack and grid
        self.download_button.grid(row=0, column=0, padx=10, pady=10)
        self.private_button.grid(row=2, column=0, padx=10, pady=10)
        self.share_button.grid(row=1, column=0, padx=10, pady=10)
        self.trash_button.grid(row=3, column=0, padx=10, pady=10)
        self.btn_frame.pack(side="left", fill="y", pady=100)
        self.file_list.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def display_files(self):
        """
        Method for fetching the files from the server and displaying them in the listbox
        :return:
        """
        self.file_list.insert(0, "")
        self.file_list.delete("all")
        self.files = self.get_files()
        for file in self.files:
            self.file_list.insert("END", file['filename'])

    def get_selected_file(self) -> str | None:
        """
        Method for getting the file token of the file selected in the listbox
        :return:
        """
        selection = self.file_list.get()
        for file in self.files:
            if file['filename'] == selection:
                return file['file_token']

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

    def trash(self):
        file_token = self.get_selected_file()
        if file_token:
            self.trash_file(file_token)
            self.display_files()


class ShareDialog(CTkToplevel):
    def __init__(self, master, share_func: callable, file_token: str):
        super().__init__(master=master)

        # Set the window properties
        self.title("Share")
        self.geometry("300x130")
        self.share_func = share_func
        self.file_token = file_token
        self.create_widgets()

    def create_widgets(self):
        # Create the label, entry, and button
        self.label = CTkLabel(self, text="Share with (enter username):")
        self.entry = CTkEntry(self)
        self.share_button = CTkButton(self, text="Share", command=self.share)

        # Vertical layout using pack
        self.label.pack(pady=10)
        self.entry.pack()
        self.share_button.pack(pady=5)

    def share(self):
        username = self.entry.get()
        self.share_func(self.file_token, username)
        self.destroy()
