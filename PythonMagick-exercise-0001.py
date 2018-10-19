# 동작 안 함

#from PythonMagick import *
#from PythonMagick import Image
import PythonMagick as Magick

img = Magick.Image("clipboard:").read()
img.write("clipboard.jpg")