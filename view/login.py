from customtkinter import *
import auth
from viewlist import ViewType
from prefs import preferences
from view.error_window import ErrorWindow


class Login(CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.configure(fg_color=preferences["BACKGROUND_COLOR"])
        self.create_widgets()
        self.error_window = None

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

        self.register_label.bind("<Button-1>", lambda e: self.master.changeView(ViewType.REGISTER))

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
        username = self.entry_username.get()
        password = self.entry_password.get()

        response = auth.login(username, password)
        if response[0]:
            self.master.logged_in = True
            self.master.changeView(ViewType.MENU)
        else:
            if self.error_window is None or not self.error_window.winfo_exists():
                self.error_window = ErrorWindow(self, response[1])
            else:
                self.error_window.focus()

    def guest(self):
        response = auth.get_token()
        self.master.logged_in = False
        self.master.changeView(ViewType.MENU)

    def on_key_press(self, event):
        if event.keysym == "Return":
            self.login()

    def show_password(self):
        if self.show_pass_check.get() == 1:
            self.entry_password.configure(show="")
        else:
            self.entry_password.configure(show="*")
