from tools import print_ 
class Menu:
    def __init__(self, tag, tagName):
        self.tag = tag
        self.elements = [x for x in tag if x.tag == tagName]
        self.n = len(self.desc)
        self.exitMenu = False
        
        
    @property
    def header(self):
        return "Head:\n"  
    
    
    @property
    def values(self):
        return [e.attrib for e in self.elements]
        
    
    @property    
    def tails(self):
        return ["Tail"]
        
        
    @property    
    def end(self):
        return ""    
    
    
    @property
    def desc(self):
        desc = [f"Изменить '{v}' {self.end}" for v in self.values]
        return desc + self.tails
    
    
    @property
    def customerInput(self):
        return input(f"Введите число от 1 до {self.n}: ").strip()
    
    
    def call(self):
        #Вывести меню пользователю
        print(self.__str__())
        #пользователь ввел номер меню
        _input_ = self.customerInput
        #выбор из меню из программы
        self.selectLogic(_input_)
        #если не выход из меню
        if not self.exitMenu:
            self.restart()
            
    
    def __str__(self):
        n = self.n
        out = self.header
        out += '\n'.join([f"{i+1}. {self.desc[i]}" for i in range(n)])
        return out
    
    
    def restart(self, text="", error=False):
        self.call()
    
    
    def writeError(self, error):
        print(f"{error}! Попробуйте еще раз!")
        print_()
        
        
from _xml_ import _XML_
from _xml_ import _xml_updateDirectories
class MenuCategories(Menu):    
    def __init__(self):
        self.outputStatistics = "Вывод статистики: OFF"
        super().__init__(_XML_.root, _XML_.root[0].tag)
        
    
    @property
    def header(self):
        return "\nВыберите категорию: \n"
    
    
    @property
    def values(self):
        key = self.elements[0].keys()[0] # 'type'
        return [ e.attrib[key] for e in self.elements]
    
    
    @property
    def tails(self):
        return ["Режим ручного ввода файла", "Изменить каталоги, в которых расположены файлы", self.outputStatistics,  "Выход из программы"]
    
    
    @property    
    def end(self):
        return "файлы"     
           
            
    def selectLogic(self, i):
        suffixes = self.elements
        try:
            i = int(i)
            match i:
                # вызов меню выбора файлов
                case i if i in range(1, len(suffixes) + 1 ):
                    MenuFiles(suffixes[i-1]).call()
                    
                # вызов меню пользовательского ввода
                case i if i == self.n-3: 
                    MenuCustomer(None).call()

                # изменить дирректории в XML файле   
                case i if i == self.n-2:
                    _xml_updateDirectories(suffixes)
                
                # выбор вывода статистики пользователем
                case i if i == self.n-1:
                    self.selectStatistic()

                # выход из меню 
                case i if i == self.n: 
                    self.exitMenu = True
                    
                case _:
                    self.writeError("Такой категории не существует")
        except ValueError:
            self.writeError("Вы ввели не целочисленное значение")
    
    
    def selectStatistic(self):
        if self.outputStatistics.find("ON") > 0:
            self.outputStatistics = self.outputStatistics.replace("ON", "OFF")
        else:
            self.outputStatistics = self.outputStatistics.replace("OFF", "ON")
    
    
import sys    
class MenuFiles(Menu):
    def __init__(self, tag, tagName="filenames"):
        super().__init__(tag, tagName) 
        self.n = len(self.values)
        
    
    @property
    def header(self):
        return "\n\nВы зашли в меню выбора файла. Для возвращения в меню выбора категории нажмите Enter\n" + "Выберите номер файла, который будет изменен: \n"
    
    
    @property
    def values(self):
        return [e.text for e in self.elements]
    

    def selectLogic(self, i):
        try:
            match i:
                # Вернуться к выбору категории
                case "":  self.exitMenu = True              
                
                #Вызов меню пользовательского ввода
                case i if int(i) in range(1, self.n+1):  
                    fileTag = self.elements[int(i)-1]
                    MenuCustomer(fileTag).call()

                #любые другие номера или строки вызывают ошибку    
                case _:   self.writeError("Такого номера файла не существует")
        except ValueError:
            self.writeError("Вы ввели не целочисленное значение")
    
    
    def __str__(self):
        n = len(self.values)
        out = self.header
        out += '\n'.join([f"{i+1}. {self.values[i]}" for i in range(n)])
        return out


from file_handler import FileHandler
class MenuCustomer(Menu):
    def __init__(self, tag):
        super().__init__(tag, "")
        
    
    @property
    def header(self):
        return "\n\nВы зашли в меню замены строк в файле. Для возращения в прошлое меню нажмите Enter."  
    
    
    @property
    def desc(self):
        if self.tag is None:
            return "[полный_путь_к_файлу] [номер_начальной_строки] [номер_конечной_строки] [дельта]:"
        else:  
            return "[номер_начальной_строки] [номер_конечной_строки] [дельта]:"
        
        
    @property
    def customerInput(self):
        return input(f"\nВведите строку в формате {self.desc}\n").strip()
    
   
    def selectLogic(self, data):
        match data:
            # Вернуться к выбору файла
            case "":  self.exitMenu = True              
            
            #любые другие номера или строки     
            case _:   self.runBusinessLogic(data)
    
    
    def runBusinessLogic(self, data):    
        #создание файлового обработчика
        handler = FileHandler(data, self.tag)
        #запуск логики замены номеров
        handler = handler.run()
        #печатать статистику измененных номеров для пользователя
        if menuCategories.outputStatistics.find("ON") > 0:
            handler.printStatisticsNumbersChangesInFile()


    def __str__(self):
        return self.header


#Список категорий генерируется один раз
menuCategories = None
def createMenuCategories():
    global menuCategories
    if not menuCategories:
        menuCategories = MenuCategories()
    else:
        print("Категории уже существуют!")      

#C:\GitHub\Python\Python-file-assistant-tool\russ\EXAMPLE.MSG 1 16 2
#"Тестирование меню")

def test():
    _XML_.connectFile("data.xml")
    #cоздать меню выбора категории
    createMenuCategories()
    #вызов меню категорий
    menuCategories.call()   
    

def main():
    test()

if __name__ == "__main__": 
    main()        
