from backend import database
import customtkinter as ctk
from .scrolltag import ScrollTag
from abc import ABC

class SearchWindow(ctk.CTkToplevel):
    def __init__(self, master, engine, action, add_button=False):
        super().__init__(master)

        self.title("Search Tag")
        self.geometry("300x600")
        self.attributes("-topmost", True)
        self.add_button = add_button


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

        if self.add_button:
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
        self.action(name_tag)