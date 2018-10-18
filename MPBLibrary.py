import ntpath

def getFileNameFromFullPath(fullPath):
    head, tail = ntpath.split(fullPath)

    return tail or ntpath.basename(head)