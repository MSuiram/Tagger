import customtkinter as ctk
import tkinter as tk
import os
import PIL
from .buttonlist import ButtonList

class ImageFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.image = None

        self.image_label = ctk.CTkLabel(self, text="")
        self.image_label.pack(expand=True, fill="both", padx=10, pady=10)

    def new_image(self, path, filename):
        try:
            file_path = os.path.join(path, filename)

            pil_image = PIL.Image.open(file_path)

            image_size = self.image_size(pil_image)

            self.image = ctk.CTkImage(light_image=pil_image,dark_image=pil_image,size=image_size)

            self.image_label.configure(image=self.image, text="")

        except (FileNotFoundError, OSError) as e:
            print(f"Impossible de charger l'image : {e}")

    def image_size(self, image):
        width_image, height_image = image.size
        width_frame, height_frame = self.winfo_width()-20, self.winfo_height()-20

        ratio = min(width_frame/width_image, height_frame/height_image)

        if ratio >= 1:
            return (width_image, height_image)
        else:
            return (round(width_image*ratio), round(height_image*ratio))

class Window(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.path = None

        self.files = []
        self.image_index = 0

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.list_frame = ButtonList(self, items=[], on_click=self.on_item_click, row_height=42, overscan=3 )
        self.list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.main_frame = ImageFrame(self)
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.info_frame = ctk.CTkFrame(self)
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

    def on_item_click(self, filename, index):
        self.image_index = index
        self.main_frame.new_image(self.path, filename)

    def next_image(self, event=None):
        if not self.files:
            return
        self.image_index +=1
        self.main_frame.new_image(self.path, self.files[self.image_index])

    def previous_image(self, event=None):
        if not self.files:
            return
        self.image_index -=1
        self.main_frame.new_image(self.path, self.files[self.image_index])