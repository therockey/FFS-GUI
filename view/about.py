from customtkinter import *


class About(CTkToplevel):
    def __init__(self, master):
        super().__init__(master=master)
        self.create_widgets()

    def create_widgets(self):
        self.label = CTkLabel(self, text="About window")
        self.label.pack()
