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
        self.tag_list = []
        self.index = 0

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

        self.ignore_trace = False
        self.search_var.trace_add("write", self.entry_change)

        self.scroll_tag = ScrollTag(self, self.on_button_click)
        self.scroll_tag.grid(row=2, sticky="nsew")

        self.entry_change()

        self.search_entry.bind('<Tab>', self.tab_action)
        self.search_entry.bind('<Return>', self.enter_action)

    def entry_change(self, *_):
        if self.ignore_trace:
            return

        word = self.search_var.get()
        liste = database.search_tag(word, self.engine)
        self.scroll_tag.button_tags_creator(liste)
        self.tag_list = liste
        self.index = 0

    def enter_action(self, event=None):
        tag = self.search_var.get()
        if database.id_tag(tag, self.engine):
            self.action(tag)

    def tab_action(self, event=None):
        if not self.tag_list:
            return

        self.ignore_trace = True
        try:
            self.search_var.set(self.tag_list[self.index][0])
        finally:
            self.ignore_trace = False

        if self.index >= len(self.tag_list)-1:
            self.index = 0
        else:
            self.index += 1

    def add_tag(self):
        word = self.search_var.get()
        database.add_tag(word,engine=self.engine)

    def set_engine_search(self, engine):
        self.engine = engine

    def on_button_click(self, name_tag):
        self.action(name_tag)