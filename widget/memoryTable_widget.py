from functools import wraps

import customtkinter as ctk


def convert_base(base: str, value: int):
    if base.startswith("2"):
        return format(value, '#0{}b'.format(10))
    elif base.startswith("8"):
        return format(value, '#0{}o'.format(10))
    elif base.startswith("10"):
        return format(value, '#0{}'.format(10))
    elif base.startswith("16"):
        return format(value, '#0{}x'.format(10))
    else:
        return value


class MemoryTable(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.memory_table = ctk.CTkTextbox(self, state='disabled', wrap='none')
        self.memory_table.grid(row=0, column=0, sticky='nsew')

    def refresh_all(self, data: list, base: str):
        self.memory_table.configure(state='normal')
        self.memory_table.delete('0.0', 'end')
        self.memory_table.insert('0.0', self.format_data(data, base))
        self.memory_table.configure(state='disabled')

    def format_data(self, data: list, base: str):
        row = 0
        row_nb = 0
        out_text = ""
        for value in data:
            if row_nb == 0:
                out_text += f"{format(row, '#0{}'.format(3))}  "
            row_nb += 1
            out_text += convert_base(base, value) + "  "
            if row_nb == 5:
                out_text += "\n"
                row += 5
                row_nb = 0
        return out_text


