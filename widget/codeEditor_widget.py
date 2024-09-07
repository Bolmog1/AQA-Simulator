import customtkinter as ctk

from chlorophyll import CodeView
from theme import AqaLexer


class CodeEditor(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        ctk.CTkFrame.__init__(self, master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.configure(fg_color=("white", "black"))

        self.grid_propagate(False)

        scheme = "ayu-light" if self._get_appearance_mode() == "light" else "ayu-dark"

        self.codeview = CodeView(self, lexer=AqaLexer.AQALexer, color_scheme=scheme, font=("JetBrains Mono", 18), tab_width=2)
        self.codeview.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def load_script(self):
        ...

    def save_script(self):
        ...

    def get_script(self):
        return self.codeview.get("0.0", ctk.END)
