from PIL import Image
from customtkinter import *
from prefs import preferences


class Login(CTkFrame):
    def __init__(self, master,
                 login_func: callable,
                 register_view_func: callable,
                 guest_func: callable):

        super().__init__(master=master, fg_color=preferences["BACKGROUND_COLOR"])

        # Add the passed through functions for later use
        self.login_func = login_func
        self.register_view_func = register_view_func
        self.guest_func = guest_func

        self.create_widgets()

    def create_widgets(self):

        # Add the logo and title
        self.image = CTkLabel(self, text='', image=CTkImage(Image.open("./assets/icon.ico"), size=(100, 100)))
        self.title = CTkLabel(self, text="FastFileStore", font=("Segoe", 20, "bold"))

        # Add the username and password entry fields
        self.entry_username = CTkEntry(self, placeholder_text="Username")
        self.entry_username.bind("<KeyRelease>", self.on_key_press)
        self.entry_password = CTkEntry(self, show="*", placeholder_text="Password")  # show "*" for password entry
        self.entry_password.bind("<KeyRelease>", self.on_key_press)

        # Add the show password checkbox
        self.show_pass_check = CTkCheckBox(self, text="Show password", command=self.show_password, checkbox_width=15,
                                           checkbox_height=15, border_width=1)

        # Add the login and guest upload buttons
        self.button_login = CTkButton(self, text="Login", command=self.login)
        self.guest_login = CTkButton(self, text="Guest upload", command=self.guest_func)

        # Add the register button-label
        self.register_label = CTkLabel(self, text="Don't have an account? Register here", font=("Segoe", 10, "normal"))
        self.register_label.bind("<Button-1>", self.register_view_func)

        # Vertical layout using pack
        self.image.pack(pady=5)
        self.title.pack(pady=5)
        self.entry_username.pack(pady=10)
        self.entry_password.pack(pady=10)
        self.show_pass_check.pack(pady=5)
        self.register_label.pack(pady=5)
        self.button_login.pack(pady=10)
        self.guest_login.pack(pady=0)

    def login(self):
        """
        Function to log in the user through the login_func passed in the constructor
        :return:
        """
        self.login_func(self.entry_username.get(), self.entry_password.get())

    def on_key_press(self, event):
        """
        Function to handle key press events
        :param event: event object created during a keypress
        :return:
        """
        if event.keysym == "Return":
            self.login()

    def show_password(self):
        """
        Function to show the password in the password entry field if the show_pass checkbox is checked
        :return:
        """
        if self.show_pass_check.get() == 1:
            self.entry_password.configure(show="")
        else:
            self.entry_password.configure(show="*")
