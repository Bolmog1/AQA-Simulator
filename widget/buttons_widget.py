import customtkinter as ctk


class ButtonsMenu(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        ctk.CTkFrame.__init__(self, master, **kwargs)

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

        self.run = ctk.CTkButton(self, text='Run', command=lambda: self.master.get_code())
        self.run.grid(row=0, column=0, columnspan=2, sticky='ew', padx=5)

        self.load = ctk.CTkButton(self, text='Load')
        self.load.grid(row=1, column=0, sticky='ew', padx=5)

        self.unload = ctk.CTkButton(self, text='Unload')
        self.unload.grid(row=1, column=1, sticky='ew', padx=5)

        self.step = ctk.CTkButton(self, text='Step')
        self.step.grid(row=2, column=0, sticky='ew', padx=5)

        self.time = ctk.CTkEntry(self, placeholder_text="time by instr", validate='all', validatecommand=(self.vcmd, '%P'))
        self.time.grid(row=2, column=1, sticky='ew', padx=5)

        self.info = ctk.CTkButton(self, text='Documentation')
        self.info.grid(row=3, column=0, sticky='ew', padx=5)

        self.mode = ctk.CTkOptionMenu(self, values=["Décimal", "Héxadécimal"])
        self.mode.grid(row=3, column=1, sticky='ew', padx=5)

        self.debug = ctk.CTkTextbox(self, state='disabled', height=1)
        self.debug.grid(row=4, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
