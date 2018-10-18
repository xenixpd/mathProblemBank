from tkinter import *
from tkinter import ttk

root = Tk()

treeview = ttk.Treeview(root)
treeview.pack()

treeview.insert('', '0', 'item1', text='Frist Item')
treeview.insert('', '1', 'item2', text='Second Item')
treeview.insert('', '2', 'item3', text='Third Item')

root.mainloop()