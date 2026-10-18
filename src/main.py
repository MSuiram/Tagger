import customtkinter as ctk
import tkinter as tk

from frontend import menubar, window
from backend import database

ctk.set_appearance_mode("System")

ctk.set_default_color_theme("green")

appWidth, appHeight = 1920, 1080

class App(ctk.CTk):
    def set_path_folder(self, value):
            self.path_folder = value
            self.window_frame.new_path(value)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path_folder = None
        self.engine = None

        self.title("Tagger")
        self.geometry(f"{appWidth}x{appHeight}")

        # Menu
        self.menu = menubar.MenuBar(self, self, self.set_path_folder, self.set_engine)
        self.menu.pack(side="top", fill="x")
        self.menu.configure(fg_color="transparent")
        self.menu.lift()

        # Window
        self.window_frame = window.Window(self)
        self.window_frame.pack(
            side="top",
            fill="both",
            expand=True
        )

        self.bind("<Right>", self.window_frame.next_image)
        self.bind("<Left>", self.window_frame.previous_image)

    def set_engine(self,path):
        print("here")
        self.engine = database.creat_db(path)
        self.menu.set_engine_menu(self.engine)


if __name__ == "__main__":
    app = App()
    app.mainloop()