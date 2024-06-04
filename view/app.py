from customtkinter import *
from view import *
from PIL import Image
from prefs import preferences
from SlickCTk.slick_context_menu import SlickContextMenu


class App(CTk):
    def __init__(self, home_button_func: callable):
        super().__init__(fg_color=preferences["BACKGROUND_COLOR"])

        self.current_ui = []

        self.title("FastFileStore")
        self.iconbitmap(preferences["ICON_PATH"])
        self.resizable(False, False)
        self.home_btn_func = home_button_func

        self.pref_window = None
        self.about_window = None
        self.home_btn = None

    def home_button(self, switch: bool):
        if switch:
            self.home_btn = CTkButton(self, text="",
                                      image=CTkImage(Image.open("./assets/home.webp"),
                                                     size=(25, 25)),
                                      width=50, height=50,
                                      command=self.home_btn_func)
            self.home_btn.place(x=10, y=10, anchor=NW)
        else:
            if self.home_btn is not None:
                self.home_btn.destroy()
                self.home_btn = None
