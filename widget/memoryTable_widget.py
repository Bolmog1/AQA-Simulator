import customtkinter as ctk


class MemoryTable(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        for i in range(1, 41):
            self.grid_rowconfigure(i, weight=1)

        self.memory = []
        for i in range(0, 41):
            self.memory.append(ctk.CTkLabel(self, text=str(i)))
            self.memory[i].grid(row=i, column=0, sticky='nsw')