from tkinter import StringVar

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

        self.input = ctk.CTkEntry(self, placeholder_text='Wait for input', state='disabled')
        self.input.grid(row=1, column=0, pady=5, padx=5, sticky='nsew')

        self.input.bind('<Return>', self.new_entry)

    def waitForEntry(self):
        self.input.configure(state='normal')
        self.input.focus()

    def new_entry(self, e):
        self.master.entry = self.input.get()
        self.input.delete(0, 'end')
        self.input.configure(state='disabled')

    def output_msg(self, msg: str):
        self.output.configure(state='normal')
        self.output.insert("end", msg)
        self.output.configure(state='disabled')

    def reset_IO(self):
        self.output.configure(state='normal')
        self.output.delete(0.0, "end")
        self.output.configure(state='disabled')
        self.input.configure(state='normal')
        self.input.delete(0, "end")
        self.input.configure(state='disabled')