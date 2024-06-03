import datetime
import webbrowser
from tkinter import DoubleVar
import auth
from auth import login as auth_login, register as auth_register
from file_ops import *
from view import *
from viewlist import ViewType


class Controller:
    def __init__(self):
        self.app = App(lambda: self.change_view(ViewType.MENU))
        self.session = None
        self.session_expiry = None
        self.curr_view = None

    def run(self):
        self.change_view(ViewType.LOGIN)
        if not auth.check_connection():
            popup = PopupWindow(self.app,
                                "Server not reachable. Please try again later.", "Error",
                                lambda: self.app.quit())
        self.app.mainloop()

    def change_view(self, view: ViewType):
        if self.curr_view is not None:
            self.curr_view.destroy()
            self.app.current_ui.clear()

        default_layout = True

        match view:
            case ViewType.LOGIN:
                self.app.geometry("450x450")
                self.curr_view = Login(self.app, self.login,
                                       lambda: self.change_view(ViewType.REGISTER),
                                       self.guest)
                self.app.home_button(False)

            case ViewType.REGISTER:
                self.app.geometry("450x500")
                self.curr_view = Register(self.app, self.register, lambda: self.change_view(ViewType.LOGIN))
                self.app.home_button(False)

            case ViewType.MENU:
                self.app.geometry("800x450")
                self.curr_view = Menu(self.app, self.change_view)
                self.app.home_button(False)

            case ViewType.UPLOAD:
                self.app.geometry("800x400")
                self.curr_view = Upload(self.app, self.upload)
                self.app.home_button(True)

            case ViewType.FILE_LIST:
                self.app.geometry("800x450")
                files = auth.get_file_list(self.session)
                self.curr_view = MyFiles(self.app,
                                         files,
                                         self.download,
                                         self.share,
                                         self.private,
                                         self.delete)
                self.app.home_button(True)

                default_layout = False
                self.curr_view.pack(side="right", fill="both", expand=True)

            case ViewType.SHARED_FILES:
                self.app.geometry("800x450")
                files = []
                self.curr_view = SharedFiles(self.app,
                                             files,
                                             self.download)
                self.app.home_button(True)

                default_layout = False
                self.curr_view.pack(side="right", fill="both", expand=True)

        if default_layout:
            self.curr_view.grid(row=0, column=0, sticky="")
            self.app.grid_rowconfigure(0, weight=1)
            self.app.grid_columnconfigure(0, weight=1)

        self.app.current_ui.append(self.curr_view)

    def login(self, username: str, password: str):
        status, session, session_expiry = auth_login(username, password)

        if status:
            self.session = session
            self.session_expiry = session_expiry
            self.change_view(ViewType.MENU)
        else:
            popup = PopupWindow(self.app, session, "Error")

    def register(self, username: str, password: str):
        status, message = auth_register(username, password)

        status_str = "Success" if status else "Error"
        message = message if not status else "Registration successful"

        popup = PopupWindow(self.app, message, status_str)

        if status:
            self.change_view(ViewType.LOGIN)

    def guest(self):
        self.change_view(ViewType.UPLOAD)
        self.app.home_button(False)

    def upload(self, file_path: str, var: DoubleVar):
        if self.check_expiration():
            return

        url = upload_file(file_path, var, self.session)

        print(f"URL: {url}")

        post_upload = PostUpload(self.app, url)
        post_upload.focus()
        post_upload.grab_set()

    def delete(self, file_token: str):
        if self.check_expiration():
            return

        response_msg = delete_file(file_token, self.session)

        popup = PopupWindow(self.app, response_msg, "Info")

    def download(self, file_token: str):
        webbrowser.open(f"{preferences['API_URL']}/download/{file_token}")

    def share(self, file_token: str, user: str):
        if self.check_expiration():
            return

        response_msg = share_file(file_token, user, self.session)

        # Open a popup window with the response
        popup = PopupWindow(self.app, response_msg, "Info")

    def private(self, file_token: str):
        if self.check_expiration():
            return

        response_msg = private_file(file_token, self.session)

        popup = PopupWindow(self.app, response_msg, "Info")

    def check_expiration(self):
        if datetime.datetime.utcnow() < self.session_expiry:
            return False

        popup = PopupWindow(self.app, "Session expired. Please login again.", "Info")
        self.change_view(ViewType.LOGIN)
        return True
