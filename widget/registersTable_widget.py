import customtkinter as ctk
from customtkinter import CTkLabel


class RegistersTable(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        ctk.CTkFrame.__init__(self, master, **kwargs)

        self.configure()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        self.grid_propagate(False)

        for i in range(0, 13):
            self.grid_rowconfigure(i, weight=1)

        self.pc = CTkLabel(self, text="PC")
        self.pc.grid(row=0, padx=5, column=0)

        for i in range(0, 13):
            self.register = CTkLabel(self, text=f"R{i}")
            self.register.grid(row=i+1, column=0, padx=5, sticky="nswe")
            self.register.grid_propagate(False)

        self.PC = CTkLabel(self, text="No script loaded")
        self.PC.grid(row=0, column=1, sticky="nsw")

        self.registers: list[ctk.CTkLabel, ] = []
        for i in range(0, 13):
            self.registers.append(CTkLabel(self, text="0"))
            self.registers[-1].grid(row=i + 1, column=1, sticky="nsw")

    def convert_base(self, base: str, value: int):
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

    def refresh(self, registers: dict, format: str) -> None:
        self.PC.configure(text=registers["PC"])
        for i, register in enumerate(self.registers):
            register.configure(text=self.convert_base(format, registers[f"R{i}"]))
