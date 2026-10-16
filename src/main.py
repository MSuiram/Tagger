import customtkinter as ctk
import tkinter as tk

from frontend import menubar, window

ctk.set_appearance_mode("System")

ctk.set_default_color_theme("green")

appWidth, appHeight = 1920, 1080

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Tagger")
        self.geometry(f"{appWidth}x{appHeight}")


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        #Menu
        self.menu = menubar.MenuBar(self)
        self.menu.grid(row=0, column=0, padx=0, pady=(0, 0), sticky="new")
        self.menu.configure(fg_color="transparent")

        #Window
        self.window_frame = window.Window(self)
        self.window_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()