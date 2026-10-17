import customtkinter as ctk
import tkinter as tk
import CTkMenuBarPlus as ctkm

class MenuBar(ctkm.CTkMenuBar):
    def __init__(self, master):
        super().__init__(master)

        self.file_but = self.add_cascade("File")


        self.file_menu = ctkm.CustomDropdownMenu(widget=self.file_but)

        self.file_menu.add_option(
            option="Open",
            command=self.open_file
        )

        self.file_menu.add_option(
            option="Save",
            command=self.save_file
        )

    def open_file(self):
        print("Open")

    def save_file(self):
        print("Save")
        
        