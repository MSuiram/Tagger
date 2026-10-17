import customtkinter as ctk
import tkinter as tk
import os

class ButtonList(ctk.CTkFrame):
    def __init__(
        self,
        master,
        items,
        on_click=None,
        row_height=42,
        overscan=3,
        **kwargs
    ):
        super().__init__(master, **kwargs)

        self.items = items
        self.on_click = on_click
        self.row_height = row_height
        self.overscan = overscan
        self.buttons = []
        self.windows = []
        self._refresh_job = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            self,
            highlightthickness=0,
            borderwidth=0,
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ctk.CTkScrollbar(
            self,
            orientation="vertical",
            command=self.canvas.yview
        )
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(
            yscrollcommand=self._on_scroll
        )

        self._update_scrollregion()

        self.canvas.bind(
            "<Configure>", self._schedule_refresh
        )

        # Molette Windows / macOS
        self.canvas.bind_all(
            "<MouseWheel>",
            self._on_mousewheel,
            add="+"
        )

        # Molette Linux
        self.canvas.bind_all(
            "<Button-4>",
            self._on_linux_wheel,
            add="+"
        )

        self.canvas.bind_all(
            "<Button-5>",
            self._on_linux_wheel,
            add="+"
        )

        self.after_idle(self._refresh)

    def _update_scrollregion(self):
        self.canvas.configure(
            scrollregion=(
                0,
                0,
                1,
                len(self.items) * self.row_height
            )
        )

    def _on_scroll(self, first, last):
        self.scrollbar.set(first, last)
        self._schedule_refresh()

    def _schedule_refresh(self, event=None):
        if self._refresh_job is None:
            self._refresh_job = self.after_idle(
                self._refresh
            )

    def _pointer_is_inside(self, event):
        x = self.winfo_rootx()
        y = self.winfo_rooty()

        return (
            x <= event.x_root < x + self.winfo_width()
            and
            y <= event.y_root < y + self.winfo_height()
        )

    def _on_mousewheel(self, event):
        if not self._pointer_is_inside(event):
            return

        if event.delta == 0:
            return "break"

        if abs(event.delta) >= 120:
            units = -int(event.delta / 120)
        else:
            units = -int(event.delta)

        if units:
            self.canvas.yview_scroll(units, "units")

        return "break"

    def _on_linux_wheel(self, event):
        if not self._pointer_is_inside(event):
            return

        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

        return "break"

    def _on_button_click(self, index):
        if self.on_click is not None:
            self.on_click(self.items[index])

    def _refresh(self, event=None):
        self._refresh_job = None

        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()

        if height <= 1 or width <= 1:
            return

        visible_rows = (
            height + self.row_height - 1
        ) // self.row_height

        pool_size = min(
            len(self.items),
            visible_rows + 2 * self.overscan + 1
        )

        # Créer seulement les boutons nécessaires
        while len(self.buttons) < pool_size:
            button = ctk.CTkButton(
                self.canvas,
                text="",
                height=self.row_height,
                anchor="w",
                corner_radius=6,
                command=lambda: None
            )

            window = self.canvas.create_window(
                0, 0,
                anchor="nw",
                window=button,
                width=width,
                height=self.row_height
            )

            self.buttons.append(button)
            self.windows.append(window)

        first_index = max(
            0,
            int(self.canvas.canvasy(0) // self.row_height)
            - self.overscan
        )

        for slot, (button, window) in enumerate(
            zip(self.buttons, self.windows)
        ):
            index = first_index + slot

            if index < len(self.items):
                button.configure(
                    text=str(self.items[index]),
                    command=lambda i=index:
                        self._on_button_click(i)
                )

                self.canvas.coords(
                    window,
                    0,
                    index * self.row_height
                )

                self.canvas.itemconfigure(
                    window,
                    state="normal",
                    width=width,
                    height=self.row_height
                )
            else:
                self.canvas.itemconfigure(
                    window,
                    state="hidden"
                )

    def set_items(self, items):
        self.items = items
        self._update_scrollregion()
        self.canvas.yview_moveto(0)
        self._schedule_refresh()

    
