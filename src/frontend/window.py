import customtkinter as ctk
import tkinter as tk
import os
import PIL
from .buttonlist import ButtonList
from .services import Services
from .scrolltag import ScrollTag
from backend import database

class Window(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.path = None
        self.engine = None

        self.files = []
        self.image_index = 0
        self.length_index = 0
        self.actual_files = []

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.list_frame = ButtonList(self, items=[], on_click=self.on_item_click, row_height=42, overscan=3 )
        self.list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.main_frame = ImageFrame(self, self.new_files)
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.info_frame = Services(self)
        self.info_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    def new_path(self, path):
        self.image_index = 0
        self.path = path
        print("new path")

        files_list = []

        files = os.listdir(path)

        for filename in files:
            if os.path.isfile(os.path.join(path, filename)) and filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif")):
                files_list.append(filename)

        self.list_frame.set_items(files_list)
        self.files = files_list
        self.actual_files = files_list
        self.length_index = len(files)-1

    def image_change(self, filename, index):
        try:
            file_path = os.path.join(self.path, filename)
            pil_image = PIL.Image.open(file_path)

            self.image_index = index
            self.main_frame.new_image(pil_image)

            self.info_frame.metadata(pil_image)

            database.add_image(self.path, filename, self.engine)

        except (FileNotFoundError, OSError) as e:
            print(f"Impossible de charger l'image : {e}")
            
        
    def on_item_click(self, filename, index):
        self.image_change(filename, index)

    def next_image(self, event=None):
        if not self.actual_files:
            return
        
        if self.image_index < self.length_index:
            self.image_index +=1

        self.image_change(self.actual_files[self.image_index], self.image_index)

    def previous_image(self, event=None):
        if not self.actual_files:
            return

        if self.image_index > 0:
            self.image_index -=1

        self.image_change(self.actual_files[self.image_index], self.image_index)

    def new_files(self, tags):
        self.image_index = 0

        filenames = database.find_image_for_tags(tags, self.engine)
        if filenames == []:
            self.actual_files = self.files
            self.list_frame.set_items(self.files)
            self.length_index = len(self.files)-1
        else:
            self.actual_files = filenames
            self.list_frame.set_items(filenames)
            self.length_index = len(filenames)-1
        print(filenames)

    def set_engine_window(self, engine):
        self.engine = engine
        self.info_frame.set_engine_info_frame(engine)
        self.main_frame.set_engine_image_frame(engine)

class ImageFrame(ctk.CTkFrame):
    def __init__(self, master, action):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.image = None
        self.toplevel = None
        self.engine = None
        self.tag_selected = []
        self.action = action

        self.add_tag_button = ctk.CTkButton(self, text=("Add Tag"), command=lambda: self.on_click_add_tag())
        self.add_tag_button.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.tag_frame = ScrollTag(
            self,
            orientation="horizontal",
            on_click= self.tag_reload,
            height=30,
            button_orientation="horizontal"
        )
        self.tag_frame.grid(
            row=0, column=1,
            sticky="ew",
            padx=10, pady=10
        )

        self.image_label = ctk.CTkLabel(
            self,
            text="Aucune image"
        )
        self.image_label.grid(
            row=1, column=0,
            columnspan=2,
            sticky="nsew",
            padx=10, pady=10
        )

    def new_image(self, pil_image):
        self.update_idletasks()

        image_size = self.image_size(pil_image)

        self.image = ctk.CTkImage(
            light_image=pil_image,
            dark_image=pil_image,
            size=image_size
        )

        self.image_label.configure(
            image=self.image,
            text=""
        )

    def image_size(self, image):
        width_image, height_image = image.size

        width_frame = max(1, self.winfo_width() - 40)
        height_frame = max(1, self.winfo_height() - 90)

        ratio = min(
            width_frame / width_image,
            height_frame / height_image,
            1
        )

        return (
            round(width_image * ratio),
            round(height_image * ratio)
        )

    def on_click_add_tag(self):
        if self.toplevel is None or not self.toplevel.winfo_exists():
            self.toplevel = SearchWindow(self, self.engine, self.tag_reload)
        else:
            self.toplevel.destroy()
            self.toplevel = SearchWindow(self, self.engine, self.tag_reload)

    def tag_reload(self, new_tag):
        if [new_tag] in self.tag_selected:
            self.tag_selected.remove([new_tag])
        else:
            self.tag_selected.append([new_tag])

        self.action(self.tag_selected)

        self.tag_frame.button_tags_creator(self.tag_selected)

    def set_engine_image_frame(self, engine):
        self.engine=engine

class SearchWindow(ctk.CTkToplevel):
    def __init__(self, master, engine, action):
        super().__init__(master)

        self.title("Search Tag")
        self.geometry("300x600")
        self.attributes("-topmost", True)


        self.engine = engine
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

        self.search_var.trace_add("write", self.entry_change)

        self.scroll_tag = ScrollTag(self, self.on_button_click)
        self.scroll_tag.grid(row=2, sticky="nsew")

        self.entry_change()

    def entry_change(self, *_):
        word = self.search_var.get()
        liste = database.search_tag(word, self.engine)
        self.scroll_tag.button_tags_creator(liste)

    def set_engine_search(self, engine):
        self.engine = engine

    def on_button_click(self, name_tag):
        self.action(name_tag)