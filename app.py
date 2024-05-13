from customtkinter import *
from view.login import Login
from view.menu import Menu
from view.preferences import Preferences
from view.about import About
from viewlist import ViewType
from prefs import preferences
from SlickCTk.slick_context_menu import SlickContextMenu


class App(CTk):
    def __init__(self):
        super().__init__()

        self.current_ui = []

        self.title("FastFileStore")
        self.iconbitmap(preferences["ICON_PATH"])
        self.resizable(False, False)

        self.logged_in = False
        self.pref_window = None
        self.about_window = None

        self.main_content = Login(self)
        self.changeView(ViewType.LOGIN)

        menu_options = {
            "Preferences": self.open_settings,
            "About": self.open_about,
            "Quit": self.quit,
        }

        self.menu = SlickContextMenu(self, menu_options)

    def quit(self) -> None:
        self.destroy()

    def changeView(self, view: ViewType) -> None:
        if self.main_content is not None or not self.main_content.winfo_exists():
            self.main_content.destroy()
            self.current_ui.clear()

        match view:
            case ViewType.LOGIN:
                self.geometry("450x450")
                self.main_content = Login(self)
                self.main_content.grid(row=0, column=0, sticky="")
                self.grid_rowconfigure(0, weight=1)
                self.grid_columnconfigure(0, weight=1)
                self.current_ui.append(self.main_content)
            case ViewType.MENU:
                self.geometry("800x450")
                self.main_content = Menu(self)
                self.main_content.pack(expand=True, fill=BOTH)
                self.current_ui.append(self.main_content)

            case ViewType.UPLOAD:
                pass
            case ViewType.FILE_LIST:
                pass

    @property
    def login_status(self):
        return self.logged_in

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


if __name__ == "__main__":
    app = App()
    app.mainloop()
