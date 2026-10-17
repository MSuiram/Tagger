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

        # Menu
        self.menu = menubar.MenuBar(self)
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


if __name__ == "__main__":
    app = App()
    app.mainloop()