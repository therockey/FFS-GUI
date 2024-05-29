from customtkinter import *
from view.preferences import Preferences
from view.about import About
from prefs import preferences
from SlickCTk.slick_context_menu import SlickContextMenu


class App(CTk):
    def __init__(self, home_button_func: callable):
        super().__init__()

        self.configure(fg_color=preferences["BACKGROUND_COLOR"])

        self.current_ui = []

        self.title("FastFileStore")
        self.iconbitmap(preferences["ICON_PATH"])
        self.resizable(False, False)
        self.home_btn_func = home_button_func

        self.pref_window = None
        self.about_window = None
        self.home_btn = None

        menu_options = {
            "Preferences": self.open_settings,
            "About": self.open_about,
            "Quit": self.quit,
        }

        self.menu = SlickContextMenu(self, menu_options)

    def quit(self) -> None:
        self.destroy()

    def open_settings(self):
        if self.pref_window is None or not self.pref_window.winfo_exists():
            self.pref_window = Preferences(self)
        else:
            self.pref_window.focus()

    def open_about(self):
        if self.about_window is None or not self.about_window.winfo_exists():
            self.about_window = About(self)
        else:
            self.about_window.focus()

    def home_button(self, switch: bool):
        if switch:
            self.home_btn = CTkButton(self, text="Home", command=self.home_btn_func)
            self.home_btn.place(x=0, y=0, anchor=NW)
        else:
            self.home_btn.destroy()
            self.home_btn = None
