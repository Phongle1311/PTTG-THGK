import tkinter as tk
import GUI
from GUI.MainApplication import MainApplication


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
