#from tkinter import *
from PIL import ImageTk, Image, ImageFile

img = Image.open(".\\test.gif")
#image = ImageTk.PhotoImage(img)
#img.save(".\\test.png", "png")
img.convert('RGB').save(".\\test.jpg")