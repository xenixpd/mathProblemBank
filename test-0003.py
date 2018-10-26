import tkinter as tk
from tkinter import filedialog
from openpyxl import load_workbook

root = tk.Tk()
root.title("엑셀로부터 문제 등록하기")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

sheetList = tk.Listbox(root)
sheetList.pack()

# 그림을 찾을 폴더를 선택
excelFilename = filedialog.askopenfilename(filetypes=(("Excel 파일", "*.xls; *.xlsx; *.xlsm"),))

if excelFilename != '':
    wb = load_workbook(excelFilename)
    print(wb.sheetnames)
    
    for ws in wb.sheetnames:
        sheetList.insert(tk.END, ws)

root.mainloop()