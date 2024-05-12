from customtkinter import *


class Login(CTkFrame):
    def __init__(self, master, change_color_theme):
        super().__init__(master=master)
        self.create_widgets()

    def create_widgets(self):
        # Create labels
        self.label_username = CTkLabel(self, text="Username")
        self.label_password = CTkLabel(self, text="Password", font=("Segoe", 12, "normal"))

        # Create entry fields
        self.entry_username = CTkEntry(self)
        self.entry_password = CTkEntry(self, show="*")  # show "*" for password entry

        # Create login button
        self.button_login = CTkButton(self, text="Login", command=self.login)

        # Layout using pack
        self.label_username.pack(pady=5)
        self.entry_username.pack(pady=5)
        self.label_password.pack(pady=5)
        self.entry_password.pack(pady=5)
        self.button_login.pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
