import customtkinter as ctk
import tkinter as tk
import os
from PIL import Image
from PIL.ExifTags import TAGS
from backend import database
from .scrolltag import ScrollTag

class Services(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.toplevel = None
        self.engine = None
        self.filename = None

        self.metadatabox = ctk.CTkLabel(self, compound="left", width=400, padx= 10, pady=10, justify= "left", anchor="w")
        self.metadatabox.grid(row = 0, column= 0, sticky="new")
        self.metadatabox.configure(text = "Aucune métadonnée")

        self.addtag_button = ctk.CTkButton(self, text="Ajouter un Tag", height=42, command=lambda: self.search_window())
        self.addtag_button.grid(row=1, column= 0, sticky="nsew", padx=10, pady=10 )

        self.tag_list= ScrollTag(self, on_click=self.tag_click)
        self.tag_list.grid(row=2, column= 0, sticky="nsew")
    
    def metadata(self, image):
        self.filename = os.path.basename(image.filename)

        self.tag_reload()

        exifdata = image.getexif()

        text = f"Filename: {self.filename}\n"

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
            text += "Aucune métadonnée EXIF trouvée pour cette image.\n"
            self.metadatabox.configure(text = text)

    def search_window(self):
        if self.toplevel is None or not self.toplevel.winfo_exists():
            self.toplevel = SearchWindow(self, self.engine, self.filename, self.tag_reload)
        else:
            self.toplevel.destroy()
            self.toplevel = SearchWindow(self, self.engine, self.filename, self.tag_reload)

    def set_engine_info_frame(self, engine):
        self.engine = engine

    def tag_reload(self):
        tag_list = database.find_tag_for_image(self.filename, self.engine)
        self.tag_list.button_tags_creator(tag_list)

    def tag_click(self, tag_name):
        print(tag_name)


class SearchWindow(ctk.CTkToplevel):
    def __init__(self, master, engine, filename, action):
        super().__init__(master)

        self.title("Search Tag")
        self.geometry("300x600")
        self.attributes("-topmost", True)


        self.engine = engine
        self.filename = filename
        self.action = action
        self.search_var = ctk.StringVar()

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="Search...",
            textvariable=self.search_var
        )
        self.search_entry.grid(row=0, sticky="new")

        self.add_tag_button = ctk.CTkButton(self, text="New Tag", command=lambda: self.add_tag())
        self.add_tag_button.grid(row=1, sticky="new")

        self.search_var.trace_add("write", self.entry_change)

        self.scroll_tag = ScrollTag(self, self.on_button_click)
        self.scroll_tag.grid(row=2, sticky="nsew")

        self.entry_change()

    def entry_change(self, *_):
        word = self.search_var.get()
        liste = database.search_tag(word, self.engine)
        self.scroll_tag.button_tags_creator(liste)

    def add_tag(self):
        word = self.search_var.get()
        database.add_tag(word,engine=self.engine)

    def set_engine_search(self, engine):
        self.engine = engine

    def on_button_click(self, name_tag):
        image = database.id_image(self.filename, self.engine)
        tag = database.id_tag(name_tag, self.engine)

        if database.id_link_image_tag(image, tag, self.engine) is None:
            database.add_link_image_tag(self.filename, name_tag, self.engine)
        else:
            database.delete_link_image_tag(self.filename, name_tag, self.engine)

        self.action()

        
