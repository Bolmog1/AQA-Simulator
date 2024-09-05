import customtkinter as ctk
from outils import *
from widget import *
from widget.IO_widget import IO
from widget.buttons_widget import ButtonsMenu
from widget.codeEditor_widget import CodeEditor
from widget.memoryTable_widget import MemoryTable
from widget.registersTable_widget import RegistersTable


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AQA Interpreter")
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

    def get_code(self):
        print(self.codeEditor.get_script())


if __name__ == "__main__":
    app = App()
    app.mainloop()
