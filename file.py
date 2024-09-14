from tkinter import filedialog


def open_file() -> str:
    filename = filedialog.askopenfile(mode='r', filetypes=[("Text File", ".txt"), ("Assembly Script", [".aqa", ".asm"])])
    return filename.read()


def save_file(text: str):
    filename = filedialog.asksaveasfile(defaultextension=".aqa", filetypes=[("Assembly Script", ".aqa"), ("Text File", ".txt")])
    filename.write(text)