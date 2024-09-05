def setup_Window_Size(parent):
    h, w = parent.winfo_screenheight(), parent.winfo_screenwidth()
    parent.geometry(f"{round(w*2/3)}x{round(h*2/3)}")
