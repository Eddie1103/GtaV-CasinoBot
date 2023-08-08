import tkinter as tk

def GetScreenSize():
    root = tk.Tk()
    return root.winfo_screenwidth(), root.winfo_screenheight()