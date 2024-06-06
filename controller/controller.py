import datetime
import webbrowser
from tkinter import DoubleVar
import auth
from auth import login as auth_login, register as auth_register
from file_ops import *
from view import *
from viewlist import ViewType
from prefs import preferences


class Controller:
    def __init__(self):
        self.app = App(lambda: self.change_view(ViewType.MENU),
                       lambda: self.change_view(ViewType.LOGIN))
        self.session = None
        self.session_expiry = None
        self.curr_view = None

    def run(self):
        self.change_view(ViewType.LOGIN)

        # Check if the server is reachable
        if not auth.check_connection():
            PopupWindow(self.app,
                        "Server not reachable. Please try again later.", "Error",
                        lambda: self.app.destroy())
        self.app.mainloop()

    def change_view(self, view: ViewType):
        """
        Method for changing the current view of the application.
        :param view: a value of the ViewType enum corresponding to the view to change to
        :return:
        """

        # Destroy the current view if it exists
        if self.curr_view is not None:
            self.curr_view.destroy()
            self.app.current_ui.clear()

        default_layout = True

        # Switch case for changing the view
        match view:
            case ViewType.LOGIN:
                self.app.geometry("450x450")
                self.curr_view = Login(self.app, self.login,
                                       lambda e: self.change_view(ViewType.REGISTER),
                                       self.guest)
                self.app.home_button(False)
                self.app.login_btn(False)

            case ViewType.REGISTER:
                self.app.geometry("450x500")
                self.curr_view = Register(self.app, self.register, lambda e: self.change_view(ViewType.LOGIN))
                self.app.home_button(False)
                self.app.login_btn(False)

            case ViewType.MENU:
                self.app.geometry("900x450")
                self.curr_view = Menu(self.app, self.change_view, self.logout)
                self.app.home_button(False)
                self.app.login_btn(False)

            case ViewType.UPLOAD:
                self.app.geometry("400x400")
                self.curr_view = Upload(self.app, self.upload)
                self.app.home_button(True)
                self.app.login_btn(False)

            case ViewType.FILE_LIST:
                self.app.geometry("800x450")
                self.curr_view = MyFiles(self.app,
                                         lambda: auth.get_file_list(self.session),
                                         self.download,
                                         self.share,
                                         self.private,
                                         self.trash)
                self.app.home_button(True)
                self.app.login_btn(False)

                default_layout = False
                self.curr_view.pack(side="right", fill="both", expand=True)

            case ViewType.SHARED_FILES:
                self.app.geometry("800x450")
                self.curr_view = SharedFiles(self.app,
                                             lambda: auth.get_shared_file_list(self.session),
                                             self.download)
                self.app.home_button(True)
                self.app.login_btn(False)

                default_layout = False
                self.curr_view.pack(side="right", fill="both", expand=True)

            case ViewType.TRASHED_FILES:
                self.app.geometry("800x450")
                self.curr_view = TrashedFiles(self.app,
                                              lambda: auth.get_trashed_file_list(self.session),
                                              self.delete_permanently,
                                              self.restore)
                self.app.home_button(True)
                self.app.login_btn(False)

                default_layout = False
                self.curr_view.pack(side="right", fill="both", expand=True)

        # If the view has a default layout, apply a grid layout to it
        if default_layout:
            self.curr_view.grid(row=0, column=0, sticky="")
            self.app.grid_rowconfigure(0, weight=1)
            self.app.grid_columnconfigure(0, weight=1)

        self.app.current_ui.append(self.curr_view)

    def login(self, username: str, password: str):
        status, session, session_expiry = auth_login(username, password)

        # If the login was successful, set the session and change the view to the menu
        if status:
            self.session = session
            self.session_expiry = session_expiry
            self.change_view(ViewType.MENU)
        else:
            PopupWindow(self.app, session, "Error")

    def register(self, username: str, password: str):
        status, message = auth_register(username, password)

        status_str = "Success" if status else "Error"
        message = message if not status else "Registration successful"

        PopupWindow(self.app, message, status_str)

        # If the registration was successful, change the view back to the login screen
        if status:
            self.change_view(ViewType.LOGIN)

    def logout(self):
        if self.session is not None:
            if auth.logout(self.session):
                self.session = None
                self.session_expiry = None
                self.change_view(ViewType.LOGIN)
            else:
                PopupWindow(self.app, "Logout failed", "Error")
        else:
            PopupWindow(self.app, "No active session", "Error")
            self.change_view(ViewType.LOGIN)

    def guest(self):
        self.change_view(ViewType.UPLOAD)
        self.app.home_button(False)
        self.app.login_btn(True)

    def upload(self, file_path: str, var: DoubleVar, password: str | None):
        if self.check_expiration():
            return

        if password is not None and len(password) == 0:
            PopupWindow(self.app, "Password cannot be empty", "Error")
            return

        status, content = upload_file(file_path, var, self.session, password)

        if status:
            post_upload = PostUpload(self.app, content, self.curr_view.clear_selection)
            post_upload.focus()
            post_upload.grab_set()
        else:
            PopupWindow(self.app, content, "Error")

    def trash(self, file_token: str):
        if self.check_expiration():
            return

        status, response_msg = trash_file(file_token, self.session)

        header = "Info" if status else "Error"

        # Open a popup window with the response
        PopupWindow(self.app, response_msg, header)

    def download(self, file_token: str):
        # Open the download link in the default web browser, which will then handle the download
        webbrowser.open(f"{preferences['API_URL']}/file/{file_token}")

    def share(self, file_token: str, user: str):
        if self.check_expiration():
            return

        status, response_msg = share_file(file_token, user, self.session)

        header = "Info" if status else "Error"

        # Open a popup window with the response
        PopupWindow(self.app, response_msg, header)

    def private(self, file_token: str):
        if self.check_expiration():
            return

        status, response_msg = private_file(file_token, self.session)

        header = "Info" if status else "Error"

        # Open a popup window with the response
        PopupWindow(self.app, response_msg, header)

    def delete_permanently(self, file_token: str):
        if self.check_expiration():
            return

        status, response_msg = delete_file(file_token, self.session)

        header = "Info" if status else "Error"

        # Open a popup window with the response
        PopupWindow(self.app, response_msg, header)

    def restore(self, file_token: str):
        if self.check_expiration():
            return

        status, response_msg = restore_file(file_token, self.session)

        header = "Info" if status else "Error"

        # Open a popup window with the response
        PopupWindow(self.app, response_msg, header)

    def check_expiration(self):
        """
        Method for checking if the session has expired.
        :return:
        """
        if self.session is None:
            return False

        if datetime.datetime.utcnow() < self.session_expiry:
            return False

        PopupWindow(self.app, "Session expired. Please login again.", "Info")
        self.change_view(ViewType.LOGIN)
        return True
