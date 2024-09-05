import customtkinter as ctk


class IO(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        ctk.CTkFrame.__init__(self, master, **kwargs)

        self.configure(fg_color='transparent')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=50)
        self.grid_rowconfigure(1, weight=1, minsize=40)

        self.grid_propagate(False)

        self.output = ctk.CTkTextbox(self, state='disabled', height=1)
        self.output.grid(row=0, column=0, pady=10, padx=5, sticky='nsew')

        self.input = ctk.CTkEntry(self, placeholder_text='Input', state='disabled')
        self.input.grid(row=1, column=0, pady=5, padx=5, sticky='nsew')