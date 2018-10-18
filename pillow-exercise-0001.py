import tkinter as tk
from PIL import ImageTk, Image
import easygui

root = tk.Tk()

container = tk.Frame(root)
container.configure(width=400, height=240)

#imageFile = easygui.fileopenbox()
original = Image.open(easygui.fileopenbox())
resized = original.resize((400, 240), Image.ANTIALIAS)
img = ImageTk.PhotoImage(resized)
panel = tk.Label(container, image=img)
panel.config(width=400, height=240)

container.grid(row=0, column=0)
panel.grid(row=0, column=0)

root.mainloop()