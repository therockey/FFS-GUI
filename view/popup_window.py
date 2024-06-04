from customtkinter import CTkToplevel, CTkLabel, CTkButton
from prefs import preferences


class PopupWindow(CTkToplevel):
    def __init__(self, master, message="EMPTY", header="Error", additional_func=None):

        super().__init__(master=master, fg_color=preferences["BACKGROUND_COLOR"])

        # Set the window properties
        self.geometry("300x100")
        self.title(header)
        self.iconbitmap(preferences["ICON_PATH"])

        # Add the passed through functions for later use
        self.additional_func = additional_func

        self.create_widgets(message)
        self.focus()
        self.grab_set()

    def create_widgets(self, message):
        # Create the label and button
        self.label = CTkLabel(self, text=message)
        self.button = CTkButton(self, text="OK", command=self.btn_action)

        # Vertical layout using grid
        self.button.grid(row=1, column=0, pady=10, padx=10)
        self.label.grid(row=0, column=0, pady=10, padx=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def btn_action(self):
        """
        Function to be executed when the button is clicked, which can also execute any additional function passed in the constructor
        :return:
        """
        if self.additional_func is not None:
            self.additional_func()
        self.destroy()
