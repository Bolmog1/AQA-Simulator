import customtkinter as ctk
from outils import *
from widget.IO_widget import IO
from widget.buttons_widget import ButtonsMenu
from widget.codeEditor_widget import CodeEditor
from widget.memoryTable_widget import MemoryTable
from widget.registersTable_widget import RegistersTable
from main import *
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

        self.title("AQA Interpreter")
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

        self.bind_all('<Key>', self.test)

    def test(self, event):
        print(event)

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
        self.isScriptLoad = False

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
