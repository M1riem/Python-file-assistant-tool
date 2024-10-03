class Handler:
    def __init__(self, data, fileTag=None):
        self.data = data
        self.fileTag = fileTag
        self.verifiedData = None
        self.file = None
    
    def run(self):
        pass
    
    def printFile(self):
        if self.file:
            print(self.file)
    
    def printStatisticsNumbersChangesInFile(self):
        if self.file:
            print(self.file.getStatisticsNumbersChanges())
    
   
from file import File    
from input_handler import InputHandlerCustom   
class CustomFileHandler(Handler):
    def __init__(self, data):
        super().__init__(data)


    def run(self):
        #проверка входящей строки на подлинность 
        if not InputHandlerCustom.check(self.data): 
            #print("not InputHandlerCustom check")
            return None       
        
        #верные данные
        self.verifiedData = InputHandlerCustom.getVerifiedData()
        path, start, end, delta = self.verifiedData
        #открытие файла
        self.file = File(path, start, end, delta) 
        #замена номеров в файлах
        self.file.replaceNumbers()

 
from input_handler import InputHandlerUsual    
class FileFosHandler(Handler):
    def __init__(self, data, fileTag):
        super().__init__(data, fileTag)
        
    
    def run(self):
        #проверка входного формата данных на подлинность 
        if not InputHandlerUsual.check(self.data, self.fileTag): 
            #print("not InputHandlerUsual check")
            return None
        
        #верные данные
        self.verifiedData = InputHandlerUsual.getVerifiedData()
        paths, start, end, delta = self.verifiedData
        #открытие файла
        self.file = File(paths[0], start, end, delta) 
        #замена номеров в файлах
        self.file.replaceNumbers()
        
        return self.file
        
        

class FilesMSGHandler(Handler):
    def __init__(self, data, fileTag):
        super().__init__(data, fileTag)
        self.files = None
    
    
    def run(self):
        #Запуск обработчика входных данных
        if not InputHandlerUsual.check(self.data, self.fileTag): 
           # print("not InputHandlerUsual check")
            #здесь должен быть рестарт?
            return None
        
        #верные данные
        self.verifiedData = InputHandlerUsual.getVerifiedData()
        paths, start, end, delta = self.verifiedData
        
        #формирование объектов для файлов
        self.files = [File(path, start, end, delta) for path in paths]
        #сравнение файлов
        #нужно ли перенести сравнение в InputHandlerUsual?
        if self.files[0] != self.files[1]: return None
        #замена номеров в файлах
        for file in self.files:
            file.replaceNumbers()
    
        return self.files
    
    
    def printFile(self):
        if self.files:
            for file in self.files:
                print(file)
    
    def printStatisticsNumbersChangesInFile(self):
        if self.files:
            print(self.files[0].getStatisticsNumbersChanges())
    

class FileHandler():
    def __init__(self, data, fileTag = None):
        if fileTag is None:
            self.handler = CustomFileHandler(data)
        else:
            typeFile = fileTag.getparent().get('type')
            if typeFile == ".fos":
                self.handler = FileFosHandler(data, fileTag)
            else:
                self.handler = FilesMSGHandler(data, fileTag)
                
    def run(self):
        self.handler.run()
        return self.handler
    

#"Тесты для отладки модуля strategy"
#C:\GitHub\Python\Python-file-assistant-tool\russ\EXAMPLE.MSG 1 16 1
from input_handler import getImitationInputCustom 
from input_handler import getImitationInputUsual  
def test():
    mode = "Custom"
    mode = "Usual"
    fileTag = None

    if mode == "Custom":
        data = getImitationInputCustom()
    else:
        data, fileTag = getImitationInputUsual()
    
    #определение стратегии
    handler = FileHandler.process(data, fileTag)
    result = handler.run()
    
    if result is not None:
        result.printStatisticsNumbersChangesInFile()
    
    # if result is None:
        # restart()

 
def main():
    test()


if __name__ == "__main__": 
    main()
  
  
#если файлы '.MSG' не равны, то номера не заменяются
# if len(self.files) > 1 and files[0] != files[1]: return None
# if self.files[0].suffix == '.MSG' and files[0] != files[1]: return None
# for file in files:
    # file.replaceNumbers()
        
        
        
# class FileHandler():
    # @classmethod    
    # def process(cls, data, fileTag = None):
        # if fileTag is None:
            # handler = CustomFileHandler(data)
        # else:
            # typeFile = fileTag.getparent().get('type')
            # if typeFile == ".fos":
                # handler = FileFosHandler(data, fileTag)
            # else:
                # handler = FilesMSGHandler(data, fileTag)
                
        # return handler
    
