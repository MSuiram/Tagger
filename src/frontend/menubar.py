import customtkinter as ctk
import tkinter as tk
import CTkMenuBarPlus as ctkm

class MenuBar(ctkm.CTkMenuBar):
    def __init__(self, master, app, openfile_click):
        super().__init__(master)

        self.app = app

        self.openfile_click = openfile_click

        self.file_but = self.add_cascade("File")


        self.file_menu = ctkm.CustomDropdownMenu(widget=self.file_but)

        self.file_menu.add_option(
            option="Open",
            command=lambda: self.open_file(self.openfile_click)
        )

        self.file_menu.add_option(
            option="Save",
            command=self.save_file
        )

        self.label_chemin = ctk.CTkLabel(self, text="Aucun dossier sélectionné", wraplength=450)

        self.project_but = self.add_cascade("Project")

        self.project_menu = ctkm.CustomDropdownMenu(widget=self.project_but)

        self.project_menu.add_option(
            option="New Project",
            command=lambda: self.new_project()
        )

        self.project_menu.add_option(
            option="Save Project",
            command=lambda: self.save_project()
        )

        self.project_menu.add_option(
            option="Open Project",
            command=lambda: self.open_project()
        )

        self.project_menu.add_option(
            option="Close Project",
            command=lambda: self.close_project()
        )

    def open_file(self, action):
        print("Open")
        path_file = ctk.filedialog.askdirectory(title="Choisissez un dossier")
        
        if path_file:
            action(path_file)
            print(f"Dossier : {path_file}")
        else:
            print("Sélection annulée.")

    def save_file(self):
        print("Save")

    def new_project(self):
        print("New Project")

    def save_project(self):
        print("Save Project")

    def open_project(self):
        print("Open Project")

    def close_project(self):
        print("Close Project")
        
        