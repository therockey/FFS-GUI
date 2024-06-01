from customtkinter import *
from PIL import Image
from prefs import preferences
from viewlist import ViewType


class Menu(CTkFrame):
    def __init__(self, master, menu_func: callable):
        super().__init__(master=master)
        self.configure(fg_color=preferences["BACKGROUND_COLOR"])
        self.menu_func = menu_func
        self.create_widgets()

    def create_widgets(self):
        self.upload_frame = CTkFrame(self)
        self.upload_frame.configure(fg_color=preferences["BACKGROUND_COLOR"])

        self.upload_button = CTkButton(self.upload_frame, text="",
                                       image=CTkImage(Image.open("./assets/upload.webp"), size=(50, 50)), width=100,
                                       height=100, command=lambda: self.menu_func(ViewType.UPLOAD))
        self.upload_label = CTkLabel(self.upload_frame, text="Upload")

        self.upload_button.pack()
        self.upload_label.pack()
        self.upload_frame.pack(side="left", padx=25)

        self.my_files_frame = CTkFrame(self)
        self.my_files_frame.configure(fg_color=preferences["BACKGROUND_COLOR"])

        self.my_files_button = CTkButton(self.my_files_frame, text="",
                                         image=CTkImage(Image.open("./assets/my_files.webp"), size=(50, 50)), width=100, height=100,
                                         command=lambda: self.menu_func(ViewType.FILE_LIST))
        self.my_files_label = CTkLabel(self.my_files_frame, text="My Files")

        self.my_files_button.pack()
        self.my_files_label.pack()
        self.my_files_frame.pack(side="left", padx=25)

        self.shared_files_frame = CTkFrame(self)
        self.shared_files_frame.configure(fg_color=preferences["BACKGROUND_COLOR"])

        self.shared_files_button = CTkButton(self.shared_files_frame, text="",
                                             image=CTkImage(Image.open("./assets/shared_files.webp"), size=(50, 50)), width=100, height=100,
                                             command=lambda: self.menu_func(ViewType.SHARED_FILES))
        self.shared_files_label = CTkLabel(self.shared_files_frame, text="Shared Files")

        self.shared_files_button.pack()
        self.shared_files_label.pack()
        self.shared_files_frame.pack(side="left", padx=25)
