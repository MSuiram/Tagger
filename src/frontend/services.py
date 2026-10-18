import customtkinter as ctk
import tkinter as tk
import os
from PIL import Image
from PIL.ExifTags import TAGS

class Services(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.metadatabox = ctk.CTkLabel(self, compound="left", width=300, padx= 10, pady=10, justify= "left", anchor="w")
        self.metadatabox.grid(row = 0, column = 1, sticky="new")
        self.metadatabox.configure(text = "Aucune métadonnée")
    
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

