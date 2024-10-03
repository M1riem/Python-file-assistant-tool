from pathlib import Path
from tools import existFile

#подключить и проверить как работает input с рестартом, когда буду подключать Menu!

#filename =  Path(path).name, directory = Path(path).parent, suffix = Path(path).suffix 
    

#static class
class InputHandler:    
    @classmethod   
    def validN(cls, number, s):
        try:
            if int(number) >= 1:
                return True
            else:
                #menuCustomer.restart(f"{s} должен начинаться с 1 и быть целочисленным", error=True)
                #restart(f"{s} должен начинаться с 1 и быть целочисленным!")
                print(f"{s} должен начинаться с 1 и быть целочисленным!", end = " ")
                
        except:
            #menuCustomer.restart("{s} должен быть целочисленным значением")
            print(f"{s} должен быть целочисленным значением!", end = " ")
            
        return False
    
    
    @classmethod
    def validDelta(cls, delta):
        try:
            delta = int(delta)
            return True
        except:
            #menuCustomer.restart("Дельта должна быть целочисленным значением")
            print("Дельта должна быть целочисленным значением!", end = " ")
        return False    
    
    
    @classmethod
    def isStartLargerEnd(cls, start, end):
        if int(start) > int(end):    
            #menuCustomer.restart("[номер_начальной_строки] должен быть меньше или равен [номер_конечной_строки]")
            print("[номер_начальной_строки] должен быть меньше или равен [номер_конечной_строки]", end = " ")
            return True
        
        return False
    
    
    @classmethod 
    def isFailData(cls, start, end, delta):
        if not cls.validN(start, s="[номер_начальной_строки]") or not cls.validN(end, s="[номер_конечной_строки]") or not cls.validDelta(delta) or cls.isStartLargerEnd(start, end): 
            return True    
        
        return False
        
        
    @classmethod
    def notExistFile(cls, path):
        if not existFile(path):
            return True
        return False
    
    
    @classmethod 
    def _splitPath(cls, path):
        path = Path(path)
        return path.name, path.parent, path.suffix     


    @classmethod     
    def _split(cls, data):
        try:
            if len(data.split()) != 3: raise ValueError
            start, end, delta = data.split() 
            return start.strip(), end.strip(), delta.strip()
        except ValueError:
            print("Формат строки неверный!" , end = " ")
            
        return None
    
    
    @classmethod     
    def indexOutOfBoundsFile(cls, path):
        with open(path, "r") as file:
            lines = file.readlines()
            length = len(lines)
            start, end = int(cls.start), int(cls.end)
            
            numbers = [n for n in (start, end) if n > length]
            if numbers:
                print(f"Количество строк в файле '{path}': {length}. \nВы ввели номер строки: {numbers[0]}, которого не существует в файле!", end = " ")
                return True
            
        return False
    
    
    @classmethod 
    def isFailSuffix(cls, path):
        suffix = Path(path).suffix
        if suffix not in ('.fos', '.MSG'):
            print(f"Эта программа работает только с файлами имеющими расширения: '.fos', '.MSG'.", end = " ")
            return True
        
        return False
    
    
    @classmethod 
    def isFailFile(cls, path):
        # проверка файла на существование
        if cls.notExistFile(path): return True
        # проверка: [start][end] не выходят за границы файла
        if cls.indexOutOfBoundsFile(path): return True
        # проверка расширения файла 
        if cls.isFailSuffix(path): return True
 
 

from pathlib import Path    
class InputHandlerUsual(InputHandler):
    @classmethod
    def check(cls, data, fileTag):
        #проверка входных параметров
        if cls.isFailInput(data): return False
        
        #проверка [start][end][delta]
        if cls.isFailData(cls.start, cls.end, cls.delta): 
            return False
        
        #сборка paths из fileTag
        cls.paths = cls.generatePaths(fileTag)

        #проверка paths        
        for path in cls.paths:
            if cls.isFailFile(path): return False
              
        return True        
    
    
    @classmethod
    def isFailInput(cls, data):
        #разделение data на кусочки
        values = cls._split(data)
        if not values: return True
        
        cls.start, cls.end, cls.delta = values
        return False
    
    
    @classmethod     
    def generatePaths(cls, fileTag):
        filename = fileTag.text
        parent = fileTag.getparent()
        directoryTags = parent.findall("directory")
        directories = [dir.text for dir in directoryTags] 
        paths = [Path(dir)/filename for dir in directories]
        return paths
    
    
    @classmethod 
    def getVerifiedData(cls):
        return cls.paths, int(cls.start), int(cls.end), int(cls.delta)
        
        
import sys 
from pathlib import Path
class InputHandlerCustom(InputHandler):
    @classmethod
    def check(cls, data):                
        #проверка входных параметров
        if cls.isFailInput(data): return False
        
        #проверка [start][end][delta]
        if cls.isFailData(cls.start, cls.end, cls.delta): return False
        
        #проверка path
        if cls.isFailFile(cls.path): return False
        
        #сборка directory и filename из path
        #filename, directory, suffix = cls._splitPath(path)
        
        return True
      
      
    @classmethod
    def isFailInput(cls, data):
        #разделение data
        values = cls._split(data)
        if not values: return True
        
        cls.path, cls.start, cls.end, cls.delta = values
        return False
    
    
    @classmethod     
    def _split(cls, data):
        try:            
            if len(data.split()) < 4:  raise ValueError
            
            #переделать для корректного вывода ошибок!
            *path, start, end, delta = data.split()
            path = ' '.join(path)
            
            return path.strip(), start.strip(), end.strip(), delta.strip()
        except ValueError:
            #restart("Формат строки неверный")
            print("Формат строки неверный!", end = " ")
            return None


    @classmethod 
    def getVerifiedData(cls):
        return cls.path, int(cls.start), int(cls.end), int(cls.delta)



def test():
    print("Здесь можно запустить тесты для отладки класса InputHandler")
    #print("Проверка для кастомного ввода")
    #checkInputHandlerCustom()
    #print("Проверка для usual ввода, файл Fos")
    #checkInputHandlerUsualFos()
    #print("Проверка для usual ввода, файл MSG")
    #checkInputHandlerUsualMSG()


#C:\GitHub\Python\Python-file-assistant-tool\russ\EXAMPLE - копия.MSG 1 15 2
#C:\GitHub\Python\Python-file-assistant-tool\fos\_sample.fos 68 77 10
#C:\GitHub\Python\Python-file-assistant-tool\russ\EXAMPLE.MSG 1 16 2
def checkInputHandlerCustom():
    data = getImitationInputCustom()
    
    if not InputHandlerCustom.check(data): return
    
    path, start, end, delta  = InputHandlerCustom.getVerifiedData()
    
    filename, directory, suffix = InputHandler._splitPath(path)
    
    print(f"Провека прошла успешно: {type(start)}({start}), {type(end)}({end}), {type(delta)}({delta})")
    print("Файл:", path, f"\nfilename: {filename}", f"\ndirectory: {directory}", f"\nsuffix: {suffix}")
    
   
#первая задача - получить имя файла по тексту, его тэг    

def getImitationInputCustom():
    return input("Введите строку в формате [полный_путь_к_файлу] [номер_начальной_строки] [номер_конечной_строки] [дельта]:\n")
    

def getImitationInputUsual():
    _XML_.connectFile("data.xml") 
    
    tagName = input("Введите строку в формате [название файла]: ").strip()
    
    data = input("Введите строку в формате [номер_начальной_строки] [номер_конечной_строки] [дельта]:").strip()
    
    all = _XML_.tree.getiterator('filenames')    
    fileTag = [x for x in all if x.text == tagName][0]
    
    return data, fileTag


from _xml_ import _XML_    
def checkInputHandlerUsualFos():
    # имитация ввода данных
    data, fileTag = getImitationInputUsual()
    
    #если данные не верны 
    if not InputHandlerUsual.check(data, fileTag): return
    
    paths, start, end, delta  = InputHandlerUsual.getVerifiedData()
    path = paths[0]
    
    filename, directory, suffix = InputHandler._splitPath(path)
    
    print(f"Провека прошла успешно: {type(start)}({start}), {type(end)}({end}), {type(delta)}({delta})")
    print("Файл:", path, f"\nfilename: {filename}", f"\ndirectory: {directory}", f"\nsuffix: {suffix}")


from _xml_ import _XML_    
def checkInputHandlerUsualMSG():
    # имитация ввода данных
    data, fileTag = getImitationInputUsual()
    
    #если данные не верны 
    if not InputHandlerUsual.check(data, fileTag): return
    
    paths, start, end, delta  = InputHandlerUsual.getVerifiedData()
    
    filename, directory, suffix = InputHandler._splitPath(paths[0])
    directories = (directory, Path(paths[1]).parent)
    
    print(f"Провека прошла успешно: {type(start)}({start}), {type(end)}({end}), {type(delta)}({delta})")
    
    for i in range(len(paths)):
        print("Файл:", paths[i], f"\nfilename: {filename}", f"\ndirectory: {directories[i]}", f"\nsuffix: {suffix}\n")
        


def main():
    pass


if __name__ == "__main__": 
    test()