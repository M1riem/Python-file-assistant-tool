from tools import print_ 
class Menu:
    def __init__(self, tag, tagName):
        self.tag = tag
        self.elements = [x for x in tag if x.tag == tagName]
        self.n = len(self.desc)
        #self.selected?
        # debug/delete
        self.recursion = 0 
        
        
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
    
    
    def call(self):
        print(self.__str__())
        self.select()
        return self
        
    
    def __str__(self):
        n = self.n
        out = self.header
        out += '\n'.join([f"{i+1}. {self.desc[i]}" for i in range(n)])
        return out
    
    
    def restart(self, node, error=False):
        if node: print(f"{node}! Попробуйте еще раз!")
        if error: print_()
        self.call()
        
        
from _xml_ import _XML_
from _xml_ import _xml_updateDirectories
class MenuCategories(Menu):    
    def __init__(self):
        self.outputStatistics = "Вывод статистики: OFF"
        self.exitProgram = False
        
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
        return ["Режим ручного ввода файла", "Изменить каталоги, в которых расположены файлы", self.outputStatistics,  "Выход"]
    
    
    @property    
    def end(self):
        return "файлы" 
        
    
    def select(self):
        i = input(f"Введите число от 1 до {self.n}: ").strip()
        suffixes = self.elements
                    
        try:
            i = int(i)
            match i:
                #файлы '.MSG' или '.fos' из fileXML
                case i if i in range(1, len(suffixes) + 1 ):
                    #вызов меню MenuFiles и получение fileTag
                    menuFiles = MenuFiles(suffixes[i-1]).call() 
                    self.fileTag = menuFiles.fileTag
                    
                #Кастомный ввод
                case i if i == self.n-3: 
                    self.fileTag = None

                        
                #Изменить дирректории в XML файле   
                case i if i == self.n-2:
                    _xml_updateDirectories(suffixes)
                    #recursion
                    self.recursion += 1
                    self.restart("")
                    print("categoryMenu: updateDirectories n = ", self.recursion)
                
                #Вывод статистики
                case i if i == self.n-1:
                    self.recursion += 1
                    if self.outputStatistics.find("ON") > 0:
                        self.outputStatistics = self.outputStatistics.replace("ON", "OFF")
                    else:
                        self.outputStatistics = self.outputStatistics.replace("OFF", "ON")
                    self.restart("")
                    print("categoryMenu: outputStatistics n = ", self.recursion)
               
                #Выход
                case i if i == self.n: 
                    self.exitProgram = True
                    #sys.exit
                    
                #Любое другое целочисленное значение
                case _:
                    self.recursion += 1
                    self.restart("Такой категории не существует", error=True)
                    print("categoryMenu: not exist n = ", self.recursion)
        except ValueError:
            self.recursion += 1
            self.restart("Вы ввели не целочисленное значение", error=True)
            print("categoryMenu: ValueError n = ", self.recursion)
        
        return None

   
class MenuFiles(Menu):
    def __init__(self, tag, tagName="filenames"):
        super().__init__(tag, tagName) 
        self.fileTag = None
    
    @property
    def header(self):
        return "\nВыберите файл, который будет изменен: \n"  
    
    
    @property
    def values(self):
        return [e.text for e in self.elements]
        
    
    @property    
    def tails(self):
        return ["Вернуться к выбору категории"]
    
    
    def select(self):
        index = input(f"Введите число от 1 до {self.n}: ")
        
        try:
            i = int(index)
            match i:
                # Был выбран файл из списка
                case i if i in range(1, self.n):  
                    self.fileTag = self.elements[i-1]
                    print(self.fileTag.text)
                    #return self.elements[i-1]
                
                # Вернуться к выбору категории
                case i if i == self.n:
                    self.recursion += 1
                    restart(menuCategories, "")
                    print("menuFile call menuCategory: n = ", self.recursion)

                #любые другие номера или строки    
                case _:
                    #вызов этого же меню
                    self.restart("Такого номера файла не существует", error=True)
                    self.recursion += 1                    
                    print("menuFile: not exist n = ", self.recursion)
        except ValueError:
            #вызов этого же меню
            self.restart("Вы ввели не целочисленное значение", error=True)
            self.recursion += 1
            print("menuFile: ValueError n = ", self.recursion)

        
#restartMenu
def restart(menu, node, error=False):
    if node: print(f"{node}! Попробуйте еще раз!")
    if error: print_()
    menu.call()


#Список категорий генерируется один раз
menuCategories = None
def createMenuCategories():
    global menuCategories
    if not menuCategories:
        menuCategories = MenuCategories()
    else:
        print("Категории уже существуют!")        


from file_handler import FileHandler
class MenuCustomer:
    def __init__(self, fileTag):
        print(fileTag.text)
        self.fileTag = fileTag
        if fileTag is None:
            self.description =  "[полный_путь_к_файлу] [номер_начальной_строки] [номер_конечной_строки] [дельта]:\n"
        else:    
            self.description = "[номер_начальной_строки] [номер_конечной_строки] [дельта]:\n"
        
    '''    
    def select(self):
        index = input(f"Введите число от 1 до {self.n}: ")
        
        try:
            i = int(index)
            match i:
                # Был выбран файл из списка
                case i if i in range(1, self.n):  
                    return self.elements[i-1]
                
                # Вернуться к выбору категории
                case i if i == self.n:
                    self.recursion += 1
                    restart(menuCategories, "")
                    print("menuFile call menuCategory: n = ", self.recursion)

                #любые другие номера или строки    
                case _:
                    #вызов этого же меню
                    self.restart("Такого номера файла не существует", error=True)
                    self.recursion += 1                    
                    print("menuFile: not exist n = ", self.recursion)
        except ValueError:
            #вызов этого же меню
            self.restart("Вы ввели не целочисленное значение", error=True)
            self.recursion += 1
            print("menuFile: ValueError n = ", self.recursion)
            
        return None
    '''
    
    def call(self):
        #ввод данных пользователем: ([path])[start][end][delta]
        data = input(self.__str__())
        #создание файлового обработчика
        handler = FileHandler(data, self.fileTag)
        #проверка на перезапуск
        if handler is None:
            print(handler)
            self.restart()
        #запуск логики замены номеров
        handler = handler.run()
        #вывод статистики для пользователя, если это было установлено в MenuCategories
        if menuCategories.outputStatistics.find("ON") > 0:
            handler.printStatisticsNumbersChangesInFile()
    
    
    def restart(self, error=True):
        if node: print(f"! Попробуйте еще раз!")
        if error: print_()
        self.call()


    def __str__(self):
        return "\nВведите строку в формате " + self.description
    

#C:\GitHub\Python\Python-file-assistant-tool\russ\EXAMPLE.MSG 1 16 2
#"Тестирование меню")

def test():
    #вызов меню категорий
    menuCategories.call()   
    #проверка на выход из программы
    if menuCategories.exitProgram: return 
    #получаем тэг выбранного файла из меню
    fileTag = menuCategories.fileTag
    #создание меню пользовательского ввода
    #print(fileTag)
    menuCustomer = MenuCustomer(fileTag)
    #запуск menuCustomer
    menuCustomer.call()
    

def init():
    _XML_.connectFile("data.xml")
    createMenuCategories()


def main():
    init()
    test()

if __name__ == "__main__": 
    main()        
