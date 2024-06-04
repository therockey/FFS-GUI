from customtkinter import *
from prefs import preferences


class Register(CTkFrame):
    def __init__(self, master,
                 register_func: callable,
                 login_view_func: callable):

        super().__init__(master=master, fg_color=preferences["BACKGROUND_COLOR"])

        # Add the passed through functions for later use
        self.register_func = register_func
        self.login_view_func = login_view_func

        self.create_widgets()

    def create_widgets(self):

        # Create username entry field
        self.entry_username = CTkEntry(self, placeholder_text="Username")
        self.entry_username.bind("<KeyRelease>", self.on_key_press)

        # Create password entry field
        self.entry_password = CTkEntry(self, show="*", placeholder_text="Password")  # show "*" for password entry
        self.entry_password.bind("<KeyRelease>", self.on_key_press)

        # Create password repeat entry field
        self.entry_password_repeat = CTkEntry(self, show="*",
                                              placeholder_text="Repeat password")  # show "*" for password entry
        self.entry_password_repeat.bind("<KeyRelease>", self.on_key_press)

        # Create show password checkbox
        self.show_pass_check = CTkCheckBox(self, text="Show password", command=self.show_password, checkbox_width=15,
                                           checkbox_height=15, border_width=1)

        # Create login button-label
        self.login_label = CTkLabel(self, text="Already have an account? Log in here", font=("Segoe", 10, "normal"))
        self.login_label.bind("<Button-1>", self.login_view_func)

        # Create the register button
        self.button_register = CTkButton(self, text="Register",
                                         command=self.register_user,
                                         state='disabled')

        # Create password mismatch label
        self.label_password_mismatch = CTkLabel(self, text="Passwords do not match", text_color="red")
        self.label_password_mismatch.pack_forget()  # Initially hide the label

        # Vertical layout using pack
        self.entry_username.pack(pady=15)
        self.entry_password.pack(pady=5)
        self.entry_password_repeat.pack(pady=5)
        self.show_pass_check.pack(pady=5)
        self.login_label.pack(pady=5)
        self.button_register.pack(pady=10)

    def register_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        self.register_func(username, password)

    def on_key_press(self, event):
        """
        Function to handle a keypress event
        :param event: a keypress event
        :return:
        """
        if self.check_passwords() and event.keysym == "Return":
            self.register_user()

    def show_password(self):
        """
        Function to show the password in the password entry field if the show_pass checkbox is checked
        :return:
        """
        if self.show_pass_check.get() == 1:
            self.entry_password.configure(show="")
            self.entry_password_repeat.configure(show="")
        else:
            self.entry_password.configure(show="*")
            self.entry_password_repeat.configure(show="*")

    def check_passwords(self):
        """
        Function to check if the entered passwords match every time a keyboard input is detected
        :return:
        """
        password = self.entry_password.get()
        password_repeat = self.entry_password_repeat.get()

        if password == password_repeat and len(password) > 0:
            self.button_register.configure(state='normal')
            self.label_password_mismatch.pack_forget()
            return True

        self.button_register.configure(state='disabled')
        self.label_password_mismatch.pack()
        return False
