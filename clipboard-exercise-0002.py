# 성공
from tkinter import *
from PIL import ImageTk, Image, ImageGrab

root = Tk()

img = ImageGrab.grabclipboard()
original = ImageTk.PhotoImage(img)

lblImage = Label(root, image=original)
lblImage.grid(row=0, column=0)

root.mainloop()