import customtkinter as ctk
import tkinter as tk


class MenuBar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.Button1 = ctk.CTkButton(self, text="Menu")
        self.Button1.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="w")