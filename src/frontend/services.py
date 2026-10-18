import customtkinter as ctk
import tkinter as tk
import os
from PIL import Image
from PIL.ExifTags import TAGS

class Services(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.toplevel = None

        self.metadatabox = ctk.CTkLabel(self, compound="left", width=400, padx= 10, pady=10, justify= "left", anchor="w")
        self.metadatabox.grid(row = 0, column= 0, sticky="new")
        self.metadatabox.configure(text = "Aucune métadonnée")

        self.addtag_button = ctk.CTkButton(self, text="Ajouter un Tag", height=42, command=lambda: self.shearch_window())
        self.addtag_button.grid(row=1, column= 0, sticky="nsew", padx=10, pady=10 )

        self.tag_list= TagListe(self)
        self.tag_list.grid(row=2, column= 0, sticky="nsew")
    
    def metadata(self, image):
        exifdata = image.getexif()

        text = ""

        if exifdata:
            for tag_id in exifdata:
                # Obtenir le nom lisible de la balise
                tag = TAGS.get(tag_id, tag_id)
                data = exifdata.get(tag_id)

                # Décoder les données de type bytes si nécessaire
                if isinstance(data, bytes):
                    data = data.decode(errors="ignore")

                text += f"{tag}: {data}\n"

            self.metadatabox.configure(text = text)

        else:
            self.metadatabox.configure(text = "Aucune métadonnée EXIF trouvée pour cette image.")

    def shearch_window(self):
        if self.toplevel is None or not self.toplevel.winfo_exists():
            self.toplevel = ShearchWindow(self)
        else:
            self.toplevel.focus()

class TagListe(ctk.CTkScrollableFrame):
    def __init__(self, master):
            super().__init__(master)

            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)

            self.test = ctk.CTkButton(self, text="test")
            self.test.grid(row=0, column= 0, sticky="nsew")

class ShearchWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Shearch Tag")
        self.geometry("300x600")
        self.attributes("-topmost", True)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.shearch_entry = ctk.CTkEntry(self, placeholder_text="Shearch...")
        self.shearch_entry.grid(row=0, sticky="new")

        self.scroll_tag = ctk.CTkScrollableFrame(self)
        self.scroll_tag.grid(row=1, sticky="nsew")

