from customtkinter import *
from viewlist import ViewType
from prefs import preferences


class Login(CTkFrame):
    def __init__(self, master, login_func: callable, register_view_func: callable):
        super().__init__(master=master)
        self.configure(fg_color=preferences["BACKGROUND_COLOR"])
        self.login_func = login_func
        self.register_view_func = register_view_func
        self.create_widgets()

    def create_widgets(self):
        # Create labels
        self.label_username = CTkLabel(self, text="Username")
        self.label_password = CTkLabel(self, text="Password", font=("Segoe", 12, "normal"))

        # Create entry fields
        self.entry_username = CTkEntry(self)
        self.entry_username.bind("<KeyRelease>", self.on_key_press)
        self.entry_password = CTkEntry(self, show="*")  # show "*" for password entry
        self.entry_password.bind("<KeyRelease>", self.on_key_press)

        # Create show password checkbox
        self.show_pass_check = CTkCheckBox(self, text="Show password", command=self.show_password, checkbox_width=15,
                                           checkbox_height=15, border_width=1)

        # Create login button
        self.button_login = CTkButton(self, text="Login", command=self.login)
        self.guest_login = CTkButton(self, text="Guest", command=lambda: self.guest)

        self.register_label = CTkLabel(self, text="Don't have an account? Register here", font=("Segoe", 10, "normal"))

        self.register_label.bind("<Button-1>", self.register_view_func)

        # Vertical layout using pack
        self.label_username.pack(pady=0)
        self.entry_username.pack(pady=5)
        self.label_password.pack(pady=0)
        self.entry_password.pack(pady=5)
        self.show_pass_check.pack(pady=5)
        self.register_label.pack(pady=5)
        self.button_login.pack(pady=10)
        self.guest_login.pack(pady=0)

    def login(self):
        self.login_func(self.entry_username.get(), self.entry_password.get())

    def guest(self):
        self.master.changeView(ViewType.MENU)

    def on_key_press(self, event):
        if event.keysym == "Return":
            self.login()

    def show_password(self):
        if self.show_pass_check.get() == 1:
            self.entry_password.configure(show="")
        else:
            self.entry_password.configure(show="*")
