import customtkinter as ctk

class ScrollTag(ctk.CTkScrollableFrame):
    def __init__(
        self,
        master,
        on_click,
        orientation="vertical",
        height=None,
        button_orientation="vertical"
    ):
        kwargs = {"orientation": orientation}

        if height is not None:
            kwargs["height"] = height

        super().__init__(master, **kwargs)

        self.on_click = on_click
        self.button_orientation = button_orientation
        self.button_tags = []

    def button_tags_creator(self, tags):
        for bouton in self.button_tags:
            bouton.destroy()
        self.button_tags.clear()

        for tag in tags:
            bouton = ctk.CTkButton(
                self,
                text=tag[0],
                command=lambda item=tag[0]: self.on_click(item),
                width=100
            )

            if self.button_orientation == "horizontal":
                bouton.pack(side="left", padx=5, pady=5)
            else:
                bouton.pack(side="top", padx=5, pady=5, fill="x")

            self.button_tags.append(bouton)