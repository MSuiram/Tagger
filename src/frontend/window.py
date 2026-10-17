import customtkinter as ctk
import tkinter as tk
import os
import PIL

class ButtonList(ctk.CTkScrollableFrame):
    def __init__(self, master, window, path):
        super().__init__(master)

        self.window = window

        self.buttons = dict()

        self.path = path
        

        self.button_creator()

    def button_creator(self):
        files = os.listdir(self.path)
        row = 0

        for filename in files:
            if os.path.isfile(os.path.join(self.path, filename)) and filename.endswith(".png"):
                print(filename)
                button = ctk.CTkButton(self,text=filename,command=lambda f=filename: self.on_button_click(f))

                button.grid(row=row,column=0,padx=5,pady=5,sticky="ew")

                self.buttons[filename] = button
                row += 1

        self.grid_columnconfigure(0, weight=1)

    def on_button_click(self, filename):
        self.window.file_viewed = filename

class ImageFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.image = None

        self.image_label = ctk.CTkLabel(self, text="")
        self.image_label.pack(expand=True, fill="both", padx=10, pady=10)

    def new_image(self, path, filename):
        file_path = os.path.join(path, filename)
        try:
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

        self.path = r"C:\Users\mariu\Pictures\Screenshots"
        self._file_viewed = "None"

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.list_frame = ButtonList(self, self, self.path)
        self.list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.main_frame = ImageFrame(self)
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    @property
    def file_viewed(self):
        return self._file_viewed
    
    @file_viewed.setter
    def file_viewed(self, value):
        self._file_viewed = value
        self.main_frame.new_image(self.path, self.file_viewed)