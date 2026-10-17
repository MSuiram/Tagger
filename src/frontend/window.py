import customtkinter as ctk
import tkinter as tk
import os

class ButtonList(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)

        self.buttons = dict()

        self.path = "Path"

        self.button_creator()

    def button_creator(self):
        files = os.listdir(self.path)
        row = 0

        for filename in files:
            if os.path.isfile(os.path.join(self.path, filename)) and filename.endswith(".png"):
                print(filename)
                button = ctk.CTkButton(self,text=filename,command=lambda f=filename: self.on_button_click(f))

                button.grid(row=row,column=0,padx=5,pady=5,sticky="ew")

                self.buttons[filename] = button
                row += 1

        self.grid_columnconfigure(0, weight=1)

    def on_button_click(self, filename):
        print("Image sélectionnée :", filename)

class Window(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.list_frame = ButtonList(self)
        self.list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")