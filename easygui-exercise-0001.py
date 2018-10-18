import easygui
from MPBLibrary import *

fullPath = easygui.fileopenbox(title='그림 파일 선택', filetypes=["*.gif"])

print(getFileNameFromFullPath(fullPath))