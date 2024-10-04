import sys 
import re
from pathlib import Path 
from tools import print_
from create_backup import _createBackup
class File:
    def __init__(self, path, start, end, delta):
        self.path = path 
        self.start = start 
        self.end = end 
        self.delta = delta
        self.suffix = Path(path).suffix 
        self.setPattern() 
        
        self.lines = self.getLines()
        self.allNumbers = self.getAllNumbers()
        self.output = "Файл не изменен"
        
        
    def setPattern(self):
        match self.suffix:
            case ".MSG":
                self.first_char = "{"
                self.start_bracket = "{"
                self.end_bracket   = "}"
                self.pattern_number_in_brackets = r"^{[\d]+}"
                self.pattern_number = r"[\d]+"
                
            case ".fos":
                self.first_char = "" 
                self.start_bracket = "( "
                self.end_bracket   = " )"
                self.pattern_number_in_brackets = r"\([\d\ ]+\)"
                self.pattern_number = r"[\d]+"
    
        #debug
        result = f"""suffix: '{self.suffix}' 
        first_char: '{self.first_char}'       
        start_bracket: '{self.start_bracket}'
        end_bracket: '{self.end_bracket}'
        pattern: '{self.pattern_number_in_brackets}'
        pattern_number: '{self.pattern_number}'"""
        #print(result)
        #print_()
    
    
    def getLines(self):
        with open(self.path, "r") as file:            
            lines = file.readlines()
        
        return lines
    
    #all numbers in file
    def getAllNumbers(self):
        allNumbers = {}
        
        for i in range(len(self.lines)):
            if self.lines[i].startswith(self.first_char):
                n = re.search(self.pattern_number_in_brackets, self.lines[i])
                if n == None: continue
                n = n.group()             
                allNumbers[i+1] = n    
        
        return allNumbers
    
    
    # line X {number Y1} [RUS] == [ENG] line X {number Y2} -> error: Начиная со строки X[RUS] в [ENG] другой номер: Y2 вместо Y1 -> break
    def __eq__(self, other):
        if not isinstance(other, File): 
            print(f"Error: Type object {other} isn't File! Сomparison is impossible! Program is over.")
            return False 
            
        if self.suffix != ".MSG" or other.suffix != ".MSG": 
            print(f"Error: File must have the suffix '.MSG' for comparison. Program is over.")
            return False
        
        s = self.allNumbers
        o = other.allNumbers
        differences = {k: s[k] for k in s if k in o and s[k] != o[k]}
        if differences:
            key = list(differences.keys())[0]
            print(f"Error: Начиная со строки {key} в файле [RUS], в файле [ENG] другой номер: [ENG]{o[key]} вместо [RUS]{s[key]}. Конец программы")
            return False 
            #print("Всего различных строк:", len(differences))
            #print(differences)
        
        #print("Файлы равны. Можно переходить к следующему этапу.")
        return True


    #business_logic
    def replaceNumbers(self):
        #шапка вывода статистики
        self.output = f"Номера изменены на {self.delta}:\n" + f"str".center(5) + "old".center(8) + "new".rjust(7)+ "\n"
        
        lines = self.lines
        #номера списка lines идут от 0
        for i in range(self.start - 1, self.end):
            if lines[i].startswith(self.first_char):
                number_in_brackets = re.search(self.pattern_number_in_brackets, lines[i])
                
                #{}{123}{"line not according to pattern"}
                if number_in_brackets == None: continue
                number_in_brackets = number_in_brackets.group()
                
                self.output += f"{i}:".rjust(5)
                lines[i] =  self.changeNLine(number_in_brackets, lines[i])
                
        self.change(lines)

    
    def changeNLine(self, oldN, line):
        n = re.search(self.pattern_number, oldN).group()
        newN = self.start_bracket + str( int(n) + self.delta ) + self.end_bracket
        line = re.sub(self.pattern_number_in_brackets, newN, line)
        self.output += f"{oldN.center(7)} - {newN.center(7)}\n"
        return line
    
    
    def change(self, lines):
        #создание бэкапа
        _createBackup(self.path)
    
        #перезапись файла
        self.rewrite(lines)

        #печатать статистику измененных номеров для пользователя         
        #print(self.getStatisticsNumbersChanges())
        
    
    def rewrite(self, lines):    
        with open(self.path, "w") as file:
            file.writelines(lines)
        
    
    #переделать self.output для вывода пользователя по запросу из menu
    def getStatisticsNumbersChanges(self):
        return self.output.strip()
        
        
    #debug/delete
    def printStatisticsNumbersChanges(self):
        print(self.output.strip())
        print_()
    
    
    def __repr__(self):
        result = f"File: '{self.path}' \nContains numbers:\n" + "str".ljust(7) + "number\n"
        for key in self.allNumbers:
            result+= f"{key}".ljust(7) + f"{self.allNumbers[key]}\n"
        return result
       


#C:\GitHub\Python\Python-file-assistant-tool\fos\_sample.fos 68 77 10
#C:\GitHub\Python\Python-file-assistant-tool\russ\EXAMPLE.MSG 1 16 1
from input_handler import getImitationInputCustom 
from input_handler import InputHandlerCustom  
def testInputCustom():
    data = getImitationInputCustom() 
    if not InputHandlerCustom.check(data): return
    path, start, end, delta  = InputHandlerCustom.getVerifiedData()
    print(path, start, end, delta)
    file = File(path, start, end, delta)
    file.replaceNumbers()
    #print(file.getStatisticsNumbersChanges())

    
from input_handler import getImitationInputUsual 
from input_handler import InputHandlerUsual  
def testInputUsual():
    data, fileTag = getImitationInputUsual() 
    if not InputHandlerUsual.check(data, fileTag): return
    paths, start, end, delta  = InputHandlerUsual.getVerifiedData()
    #print(paths, start, end, delta)
    
    files = []
    for path in paths:
        files.append(File(path, start, end, delta))
    
    if len(files) > 1:
        if files[0] != files[1]: return
        for file in files:
            file.replaceNumbers()
    else:
        files[0].replaceNumbers()
    
    #печатать статистику измененных номеров для пользователя         
    print(files[0].getStatisticsNumbersChanges())       

    

def main():
    testInputUsual()
    return
    testInputCustom()

    
if __name__ == "__main__": 
    main()

