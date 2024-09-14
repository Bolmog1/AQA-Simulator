from tkinter import StringVar

import customtkinter as ctk


class ButtonsMenu(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        ctk.CTkFrame.__init__(self, master, **kwargs)

        self.input = StringVar()

        self.configure(fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.grid_propagate(False)

        self.vcmd = (self.register(self.callback))

        self.time_value = ctk.StringVar()

        self.run = ctk.CTkButton(self, text='Run', command=lambda: self.after(0, self.master.runButton()))
        self.run.grid(row=0, column=0, columnspan=2, sticky='ew', padx=5)

        self.load = ctk.CTkButton(self, text='Load', command=lambda: self.after(0, self.master.load_script()))
        self.load.grid(row=1, column=0, sticky='ew', padx=5)

        self.unload = ctk.CTkButton(self, text='Unload', command=lambda: self.after(0, self.master.unload_script()))
        self.unload.grid(row=1, column=1, sticky='ew', padx=5)

        self.step = ctk.CTkButton(self, text='Step', command=lambda: self.master.step_script())
        self.step.grid(row=2, column=0, sticky='ew', padx=5)

        self.time = ctk.CTkEntry(self, placeholder_text="time by instr", validate='all', validatecommand=(self.vcmd, '%P'), textvariable=self.time_value)
        self.time.grid(row=2, column=1, sticky='ew', padx=5)

        self.info = ctk.CTkButton(self, text='Documentation')
        self.info.grid(row=3, column=0, sticky='ew', padx=5)

        self.mode = ctk.CTkOptionMenu(self, values=["2 - Binaire", "8 - Octal", "10 - Décimal", "16 - Héxadécimal"], command=self.refresh_register)
        self.mode.grid(row=3, column=1, sticky='ew', padx=5)
        self.mode.set("10 - Décimal")
        self.mode.grid_propagate(False)

        self.debug = ctk.CTkTextbox(self, state='disabled', height=1)
        self.debug.grid(row=4, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

    def refresh_register(self, event):
        self.after(0, self.master.refresh_register())
        self.after(0, self.master.refresh_memory())

    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def get_mode(self):
        return self.mode.get()

    def print_debug(self, msg:str):
        self.debug.configure(state='normal')
        self.debug.delete('0.0', 'end')
        self.debug.insert('0.0', msg)
        self.debug.configure(state='disabled')

    def isRunning(self, running: bool):
        self.run.configure(text='Run' if not running else 'Stop')

    def get_sleep_time(self):
        return int(self.time_value.get()) if self.time_value.get() else 0

    def set_sleep_time(self, time: float):
        self.time_value.set(str(time))