import os
def findBCPFiles(directory, filename, formatEnd = ".bcp"):
    bcp_files = []
    
    for file in os.listdir(directory):
        if file.startswith(filename) and file.endswith(formatEnd):
            bcp_files.append(file)
    
    return bcp_files 


def getLastBackup(directory, filename, formatEnd):
    
    backups = findBCPFiles(directory, filename, formatEnd)
    backups.sort(reverse=True) #сортируем список по убыванию
    
    last_backup = backups[0] if backups != [] else None  
    return last_backup
    
    
def getFormatN(n):

    formatN = ""
    match n:
        case n if n in range(10):
            formatN = "00" + str(n)
        case n if n in range(10, 100):   
            formatN = "0" + str(n)
        case n if n in range(100, 1000): 
            formatN = str(n) 
        case _: 
            formatN = "Error"
            print("Неверный формат номера в бэкапе")
    
    return formatN


def getN( backup, filename, end ):
    try:
        if backup is None: 
            n = 0
        elif backup.startswith(filename) and backup.endswith(end):
            n = backup.replace(filename, "").replace(end, "")
            n = int(n)
        
        return n            
    except:
        print(f"Неправильный формат последнего бэкапа: {backup}. Удалите его или измените формат на 'filename 00N.bcp'")
    
    return -1
    #вопрос: критичность обработки предыдущих неправильно заданных бэкапов. Все None просто делать 001?
     

import shutil
from pathlib import Path    
def setNewBackup(directory, filename, oldBackup, formatEnd=".bcp"):
    oldN = getN(oldBackup, filename, formatEnd)
    newN = getFormatN(oldN + 1)
    
    filenameBackup = filename + " " + newN + formatEnd 
    file = Path(directory) / Path(filename)
    backup = Path(directory) / Path(filenameBackup)
    shutil.copy(file, backup)
    
    #return filenameBackup
    return backup

    
#переделать для библиотеки pathlib    
from pathlib import Path
def _createBackup(path, formatEnd=".bcp"):
    directory = str(Path(path).parent)
    filename = str(Path(path).name)
    
    lastBackup = getLastBackup(directory, filename, formatEnd)
    #print(f"Last backup: '{lastBackup}'") #filename or None
    
    newBackup = setNewBackup(directory, filename, lastBackup, formatEnd)
    
    #оптимизировать для вывода статистики в file.py
    #отказ от вывода бэкапа в статистику
    #print(f"Создан бэкап файла: \n'{newBackup}'")
    # print(f"created backup: '{newBackup}'")


def createBackup(directory, filename, formatEnd=".bcp"):
    
    lastBackup = getLastBackup(directory, filename, formatEnd)
    #print(f"Last backup: '{lastBackup}'") #filename or None
    
    newBackup = setNewBackup(directory, filename, lastBackup, formatEnd)
    print(f"Создан бэкап файла: '{newBackup}'")
    # print(f"created backup: '{newBackup}'")        


from tools import extractAllPaths
from tools import printInput
def main():
    path_file = input("Введите путь к файлу: ")
    paths = extractAllPaths(path_file)
    
    #check  
    if paths == None: return
    
    #os
    path, filename, directory = paths.values()
    
    #input
    #printInput(path, filename, directory)
    
    #output
    createBackup(directory, filename, formatEnd=".bcp")


if __name__ == "__main__": 
    main()  




'''
import os
def findAllBCPFiles(directory):
    bcp_files = []
    
    for file in os.listdir(directory):
        if file.endswith(".bcp"):
            bcp_files.append(file)
    
    return bcp_files
'''