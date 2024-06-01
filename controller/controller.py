import datetime

from auth import login as auth_login, register as auth_register
from file_ops import upload_file
from view import *
from viewlist import ViewType


class Controller:
    def __init__(self):
        self.app = App(lambda: self.change_view(ViewType.MENU))
        self.token = None
        self.session_expiry = None
        self.curr_view = None

    def run(self):
        self.change_view(ViewType.LOGIN)
        self.app.mainloop()

    def change_view(self, view: ViewType):
        if self.curr_view is not None:
            self.curr_view.destroy()
            self.app.current_ui.clear()

        match view:
            case ViewType.LOGIN:
                self.app.geometry("450x450")
                self.curr_view = Login(self.app, self.login, lambda e: self.change_view(ViewType.REGISTER))
                self.app.home_button(False)

            case ViewType.REGISTER:
                self.app.geometry("450x500")
                self.curr_view = Register(self.app, self.register, lambda e: self.change_view(ViewType.LOGIN))
                self.app.home_button(False)

            case ViewType.MENU:
                self.app.geometry("800x450")
                self.curr_view = Menu(self.app, self.change_view)
                self.app.home_button(False)

            case ViewType.UPLOAD:
                self.app.geometry("800x400")
                self.curr_view = Upload(self.app)
                self.app.home_button(True)

            case ViewType.FILE_LIST:
                self.app.geometry("800x450")
                self.curr_view = MyFiles(self.app)
                self.app.home_button(True)

        self.curr_view.grid(row=0, column=0, sticky="")
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(0, weight=1)
        self.app.current_ui.append(self.curr_view)

    def login(self, username: str, password: str):
        status, token, expiry = auth_login(username, password)

        if status:
            self.token = token
            self.session_expiry = datetime.datetime.strptime(expiry, "%Y-%m-%dT%H:%M:%S.%fZ")
            self.change_view(ViewType.MENU)

    def register(self, username: str, password: str):
        status, message = auth_register(username, password)

        status_str = "Success" if status else "Error"
        message = message if not status else "Registration successful"

        popup = PopupWindow(self.app, message, status_str)

        if status:
            self.change_view(ViewType.LOGIN)

    def upload(self, file_path: str):
        if self.check_expiration():
            return

        upload_file(file_path, self.token)
        self.change_view(ViewType.MENU)

    def check_expiration(self):
        if datetime.datetime.now(datetime.UTC) < self.session_expiry:
            return False

        popup = PopupWindow(self.app, "Session expired. Please login again.", "Info")
        self.change_view(ViewType.LOGIN)
        return True