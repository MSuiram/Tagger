import customtkinter as ctk
import tkinter as tk
import CTkMenuBarPlus as ctkm
from backend import database

class MenuBar(ctkm.CTkMenuBar):
    def __init__(self, master, app, openfile_click, set_engine):
        super().__init__(master)

        self.app = app
        self.engine = None

        self.openfile_click = openfile_click
        self.set_engine = set_engine


        #File menu
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

        self.file_menu.add_option(
            option="Add to project ",
            command=self.add_to_project_file
        )

        #Project Menu
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

    def set_engine_menu(self, engine):
        self.engine = engine

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

    def add_to_project_file(self):
        path_folder = ctk.filedialog.askdirectory(title="Choisissez un dossier")
                
        if path_folder:
            database.add_folder(path_folder, self.engine)
            self.openfile_click(path_folder)
            print(f"Dossier : {path_folder}")
        else:
            print("Sélection annulée.")
        print("Add to project")

    def new_project(self):
        path_file = ctk.filedialog.asksaveasfilename(title="Enregistez le projet sous...", defaultextension=".db")

        if path_file:
            self.set_engine(path_file)
            print(f"Dossier : {path_file}")
        else:
            print("Sélection annulée.")

        print("New Project")

    def save_project(self):
        print("Save Project")

    def open_project(self):
        path_file = ctk.filedialog.askopenfilename(title="Sélectionez un projet...")

        if path_file:
            print(f"Dossier : {path_file}")
            self.set_engine(path_file)
            folder = database.find_folder(self.engine)
            print(folder)
            self.openfile_click(folder)
        else:
            print("Sélection annulée.")

        print("Open Project")

    def close_project(self):
        print("Close Project")
        
        