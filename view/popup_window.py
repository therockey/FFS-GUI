from customtkinter import CTkToplevel, CTkLabel, CTkButton

from prefs import preferences


class PopupWindow(CTkToplevel):
    def __init__(self, master, message="EMPTY", header="Error", additional_func=None):
        super().__init__(master=master)
        self.geometry("300x100")
        self.title(header)
        self.iconbitmap(preferences["ICON_PATH"])
        self.additional_func = additional_func

        self.create_widgets(message)
        self.focus()
        self.grab_set()

    def create_widgets(self, message):
        self.label = CTkLabel(self, text=message)
        self.label.grid(row=0, column=0, pady=10, padx=10)
        self.button = CTkButton(self, text="OK", command=self.btn_action)
        self.button.grid(row=1, column=0, pady=10, padx=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def btn_action(self):
        if self.additional_func is not None:
            self.additional_func()
        self.destroy()
