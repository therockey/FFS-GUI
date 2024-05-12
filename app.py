import tkinter as tk
from customtkinter import *
from view.login import Login
from viewlist import ViewType

class App(CTk):
    def __init__(self):
        super().__init__()

        self.geometry("450x800")
        self.current_ui = []

        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        self.menu_bar.add_command(
            label='Exit',
            command=quit,
        )

        self.menu_bar.config(bg="black", fg="black")

        self.main_content = Login(self, self.change_color_theme)
        self.main_content.pack(expand=True, fill=BOTH)
        self.current_ui.append(self.main_content)

    def quit(self) -> None:
        self.destroy()

    def changeView(self, view: ViewType) -> None:
        match view:
            case ViewType.LOGIN:
                self.main_content.destroy()
                self.main_content = Login(self, self.change_color_theme)
            case ViewType.MENU:
                pass
            case ViewType.UPLOAD:
                pass
            case ViewType.FILE_LIST:
                pass




if __name__ == "__main__":
    app = App()
    app.title("FastFileStore")
    app.mainloop()
