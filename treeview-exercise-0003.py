from tkinter import *
from tkinter import ttk
import sqlite3

# MPB Classes
#from MPBUITools import MPBCurriTreeView
from MPBUITools import *

root=Tk()
root.geometry("640x480")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

#aTree = MPBUITools.MPBCurriTreeView(root, 0, 0)
aTree = MPBCurriTreeView(root, 1, 1)

root.mainloop()