import customtkinter as ctk
import tkinter as tk
import CTkMenuBarPlus as ctkm

class MenuBar(ctkm.CTkMenuBar):
    def __init__(self, master, app):
        super().__init__(master)

        self.app = app

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

        self.label_chemin = ctk.CTkLabel(self, text="Aucun dossier sélectionné", wraplength=450)

    def open_file(self):
        print("Open")
        path_file = ctk.filedialog.askdirectory(title="Choisissez un dossier")
        
        if path_file:
            self.app.path_folder = path_file
            print(f"Dossier : {path_file}")
        else:
            print("Sélection annulée.")

    def save_file(self):
        print("Save")
        
        