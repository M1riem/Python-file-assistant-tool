def print_():
    print("-" * 70)

def printInput(path, filename, directory):
    print("Input: ")
    print(f"file path: '{path}'")
    print(f"directory: '{directory}'")
    print(f"filename:  '{filename}'")
    print_() 
    
    
def changePath(path):
    return path.replace(chr(92), "/").replace(":", ":/")


def getFileName(path):
    return path.split("/")[-1]
    
    
def getDirectory(path, filename):
    return path.replace("/" + filename, "")
    
import re   
def validPath(path):
    return re.findall(r"^[a-zA-z]:\\[\w\\. +'@#$%^&()=!~`;{}\,\[\]-]+\.[a-zA-z]+", path)


def extractAllPaths(filePath):
    #clear whitespace
    filePath = filePath.strip()
    if validPath(filePath):        
        path = changePath(filePath)
        filename = getFileName(path)
        directory = getDirectory(path, filename)
        result = {"path": path, "filename": filename, "directory": directory}  
    else: 
        print("Ошибка! Неверный [полный_путь_к файлу]! Конец программы.")
        result = None
    return result


from pathlib import Path
def existFile(filename):
    if not Path(filename).is_file():
        print(f"Файл '{filename}' не существует!")
        return False

    if Path(filename).stat().st_size == 0:
        print(f"Файл '{filename}' пуст!")
        return False
    
    return True    
