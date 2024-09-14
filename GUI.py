from tkinter import Menu
import customtkinter as ctk
from outils import *
from widget.IO_widget import IO
from widget.buttons_widget import ButtonsMenu
from widget.codeEditor_widget import CodeEditor
from widget.memoryTable_widget import MemoryTable
from widget.registersTable_widget import RegistersTable
from executor import *
from file import *
import threading


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.interpreter: AqaInterpreter = AqaInterpreter(self)
        self.interpreter_thread: None | threading.Thread = None
        self.last_key_press = None

        self.isScriptLoad = False
        self.isRunning = False

        self.entry: None | str = None

        self.title("AQA Simulator")
        ctk.set_default_color_theme("./theme/green.json")
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)
        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=2)

        self.grid_propagate(False)

        setup_Window_Size(self)

        self.codeEditor = CodeEditor(self)
        self.codeEditor.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky='nsew')

        self.registersTable = RegistersTable(self)
        self.registersTable.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        self.buttonsMenu = ButtonsMenu(self)
        self.buttonsMenu.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

        self.memoryTable = MemoryTable(self)
        self.memoryTable.grid(row=0, column=2, rowspan=1, padx=10, pady=10, sticky='nsew')

        self.io = IO(self)
        self.io.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

        self.bind_all('<Key>', self.key_press)
        self.bind_all('<Command-o>', self.open)
        self.bind_all('<Command-s>', self.save)

        menu_bar = Menu(self)

        menu_file = Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Open...", command=self.open, accelerator="Cmd+O")
        menu_file.add_command(label="Save As...", command=self.save, accelerator="Cmd+S")
        menu_bar.add_cascade(label="File", menu=menu_file)

        menu_simu = Menu(menu_bar, tearoff=0)
        menu_simu.add_command(label="Run", command=self.runButton, accelerator="Cmd+R")
        menu_simu.add_command(label="Load", command=self.load_script, accelerator="Cmd+L")
        menu_simu.add_command(label="Unload", command=self.unload_script, accelerator="Cmd+U")

        menu_delay = Menu(menu_simu, tearoff=0)
        menu_delay.add_command(label="Set delay 2s", command=lambda: self.set_delay(20))
        menu_delay.add_command(label="Set delay 1s", command=lambda: self.set_delay(10))
        menu_delay.add_command(label="Set delay 0.5s", command=lambda: self.set_delay(5))
        menu_delay.add_command(label="Set no delay", command=lambda: self.set_delay(0))

        menu_simu.add_cascade(label="Delay", menu=menu_delay)
        menu_bar.add_cascade(label="Simulation", menu=menu_simu)

        menu_delay = Menu(menu_simu, tearoff=0)
        menu_delay.add_command(label="Set delay 1s", command=lambda: self.set_delay(10))
        menu_delay.add_command(label="Set delay 0.5s", command=lambda: self.set_delay(5))
        menu_delay.add_command(label="Set delay 2s", command=lambda: self.set_delay(20))
        self.config(menu=menu_bar)


    def set_delay(self, delay: float):
        self.buttonsMenu.set_sleep_time(delay)

    def save(self, e=None):
        save_file(self.codeEditor.get_script())

    def open(self, e=None):
        self.codeEditor.load_script(open_file())

    def key_press(self, event):
        if event.char:
            self.last_key_press = event.char

    def get_last_key_press(self):
        return self.last_key_press

    def reset_last_key_press(self):
        self.last_key_press = None

    def refresh_register(self):
        if self.isScriptLoad:
            self.registersTable.refresh(self.interpreter.register, self.buttonsMenu.get_mode())

    def refresh_memory(self):
        if self.isScriptLoad:
            self.memoryTable.refresh_all(self.interpreter.memory, self.buttonsMenu.get_mode())

    def load_script(self):
        self.interpreter.load(self.codeEditor.get_script())
        self.isScriptLoad = True
        self.refresh_register()
        self.refresh_memory()
        self.print_debug("Script loaded !")

    def get_format(self):
        return self.buttonsMenu.get_mode()

    def print_debug(self, msg: str):
        self.buttonsMenu.print_debug(msg)

    def unload_script(self):
        self.interpreter.unload()
        self.io.reset_IO()
        self.interpreter.unload()
        self.refresh_memory()
        self.refresh_register()
        self.isScriptLoad = False
        self.print_debug("Script unloaded !")

    def Running(self, running: bool):
        self.buttonsMenu.isRunning(running)
        self.print_debug("Script is Running" if running else "Script is Stopped")
        self.isRunning = running

    def runButton(self):
        if self.interpreter:
            if self.isRunning:
                self.isRunning = False
            else:
                self.interpreter_thread = threading.Thread(target=self.interpreter.Run)
                self.interpreter_thread.start()
        else:
            self.print_debug("No script loaded.")

    def checkThreadAlive(self):
        if self.isRunning:
            if not self.interpreter_thread.is_alive():
                self.Running(False)
                self.print_debug("Script Crashed")
            else:
                self.after(500, self.checkThreadAlive)

    def step_script(self):
        if self.interpreter and not self.isRunning and not self.interpreter.isHALT:
            self.interpreter.Step()

    def WaitForEntry(self):
        self.io.waitForEntry()

    def get_sleep_time(self):
        return self.buttonsMenu.get_sleep_time()

    def output(self, msg: str):
        self.io.output_msg(msg)



if __name__ == "__main__":
    app = App()
    app.mainloop()
