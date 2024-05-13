from customtkinter import *
from CTkColorPicker import *


def open_picker():
    picker = AskColor()
    color = picker.get()


class Preferences(CTkToplevel):
    def __init__(self, master, change_color_theme):
        super().__init__()

        self.geometry("800x450")
        self.current_ui = []

        div_frame = CTkFrame(self)
        div_frame.settings = _Settings(div_frame, change_color_theme)
        div_frame.settings.pack(expand=True, fill=BOTH)
        div_frame.color_options = _ColorOptions(div_frame)
        div_frame.color_options.pack(expand=True, fill=BOTH)

        self.main_content = div_frame
        self.main_content.pack(expand=True, fill=BOTH)
        self.current_ui.append(self.main_content)


class _Settings(CTkFrame):
    def __init__(self, master, change_color_theme):
        super().__init__(master=master)

        self.some_label = CTkLabel(self, text="Hello World")
        self.some_label.pack(pady=20)

        self.select_color_theme_optionmenu = CTkOptionMenu(self,
                                                           values=["Green", "Blue", "Dark-blue"],
                                                           command=change_color_theme)
        self.select_color_theme_optionmenu.pack()


class _ColorOptions(CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)

        self.some_label = CTkLabel(self, text="Button color")
        self.some_label.pack(pady=20)

        color = None
        self.select_color_theme_optionmenu = CTkButton(self, text="Pick color", command=open_picker)
        self.select_color_theme_optionmenu.pack()


if __name__ == "__main__":
    app = Preferences(None, None)
    app.mainloop()
