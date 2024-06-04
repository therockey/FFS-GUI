from PIL import Image
from customtkinter import *
from CTkListbox import *
from misc import format_file_size
from prefs import preferences


class TrashedFiles(CTkFrame):
    def __init__(self, master,
                 get_files: callable,
                 delete_file: callable,
                 restore_file: callable):

        super().__init__(master=master, fg_color=preferences["BACKGROUND_COLOR"])

        self.files = []

        # Add the passed through functions for later use
        self.get_files = get_files
        self.delete_file = delete_file
        self.restore_file = restore_file

        self.create_widgets()
        self.display_files()

    def create_widgets(self):

        # Create the frame to hold the buttons beside the file list
        self.btn_frame = CTkFrame(self, fg_color=preferences["BACKGROUND_COLOR"])

        # Create the buttons and file info labels
        self.filename = CTkLabel(self.btn_frame, text="Filename: ", wraplength=130)
        self.sizelabel = CTkLabel(self.btn_frame, text="Size: ")
        self.restore_button = CTkButton(self.btn_frame, text="Restore",
                                        image=CTkImage(Image.open("./assets/restore.webp")),
                                        command=self.restore)
        self.delete_button = CTkButton(self.btn_frame, text="Download",
                                       image=CTkImage(Image.open("./assets/delete.webp")),
                                       command=self.delete)

        # Create the file list
        self.file_list = CTkListbox(self, multiple_selection=False,
                                    command=lambda e: self.update_file_info())

        # Layout using pack and grid
        self.filename.grid(row=0, column=0, padx=10, pady=5)
        self.sizelabel.grid(row=1, column=0, padx=10, pady=5)
        self.restore_button.grid(row=2, column=0, padx=10, pady=10)
        self.delete_button.grid(row=3, column=0, padx=10, pady=10)
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
        Method for finding and returning the file token of the currently selected file in the listbox
        :return: file token or None if no file is selected
        """
        selection = self.file_list.get()
        for file in self.files:
            if file['filename'] == selection:
                return file['file_token']

        return None

    def delete(self):
        file_token = self.get_selected_file()
        if file_token:
            self.delete_file(file_token)
            self.display_files()

    def restore(self):
        file_token = self.get_selected_file()
        if file_token:
            self.restore_file(file_token)
            self.display_files()

    def update_file_info(self):
        """
        Method for updating the file info labels when a new file is selected in the listbox
        :return:
        """
        file = None
        selection = self.file_list.get()
        for f in self.files:
            if f['filename'] == selection:
                file = f
                break

        self.filename.configure(text=f"Filename: {file['filename']}")
        self.owner.configure(text=f"Owner: {file['owner']}")
        self.sizelabel.configure(text=f"Size: {format_file_size(file['file_size'])}")

