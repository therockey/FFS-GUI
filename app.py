from customtkinter import *
from view.login import Login
from viewlist import ViewType
from prefs import preferences


class App(CTk):
    def __init__(self):
        super().__init__()

        self.current_ui = []
        self.title("FastFileStore")
        self.resizable(False, False)

        self.main_content = Login(self)
        self.changeView(ViewType.LOGIN)

        self.iconbitmap(preferences["ICON_PATH"])

        self.logged_in = False

    def quit(self) -> None:
        self.destroy()

    def changeView(self, view: ViewType) -> None:
        match view:
            case ViewType.LOGIN:
                self.main_content.destroy()
                self.geometry("450x450")
                self.main_content = Login(self)
                self.main_content.grid(row=0, column=0, sticky="")
                self.grid_rowconfigure(0, weight=1)
                self.grid_columnconfigure(0, weight=1)
                self.current_ui.append(self.main_content)
            case ViewType.MENU:
                print("Menu")
            case ViewType.UPLOAD:
                pass
            case ViewType.FILE_LIST:
                pass

    @property
    def login_status(self):
        return self.logged_in


if __name__ == "__main__":
    app = App()
    app.mainloop()
