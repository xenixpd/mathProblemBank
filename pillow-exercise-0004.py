from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

LABEL_WIDTH = 400
LABEL_HEIGHT = 300
LABEL_RATIO = LABEL_HEIGHT/LABEL_WIDTH
       
root = Tk()
root.geometry("640x480")
#root.rowconfigure(0, weight=1)
#root.columnconfigure(0, weight=1)

# 파일 선택
selectedFileName = filedialog.askopenfilename(title='그림 파일 선택')

# 선택한 파일이 있을 때만 작업
#if selectedFileName != '':
img = Image.open(selectedFileName)
original = ImageTk.PhotoImage(img)

imageWidth = img.size[0]
imageHeight = img.size[1]
imageRatio = imageHeight/imageWidth

if imageRatio < LABEL_RATIO:
    if imageWidth > LABEL_WIDTH:
        newWidth = LABEL_WIDTH
        newHeight = int(LABEL_WIDTH * imageRatio)
    else:   # imageWidth <= LABEL_WIDTH
        newWidth = imageWidth
        newHeight = imageHeight
else:   # imageRatio >= LABEL_RATIO
    if imageHeight > LABEL_HEIGHT:
        newHeight = LABEL_HEIGHT
        newWidth = int(LABEL_HEIGHT / imageRatio)
    else:   # imageHeight <= LABEL_HEIGHT
        newHeight = imageHeight
        newWidth = imageWidth

img = img.resize((newWidth, newHeight), Image.ANTIALIAS)
resized = ImageTk.PhotoImage(img)

# 라벨(그림)
lblImage = Label(root, image=resized, bg='grey')
lblImage.config(width=400, height=300)

# 그릇에 담기
lblImage.grid(row=0, column=0, padx=5, pady=5)

root.mainloop()