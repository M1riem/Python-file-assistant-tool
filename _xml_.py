import re
from lxml import etree
from tools import existFile

class _XML_:
    filename = None
    tree = None
    root = None
    
    @classmethod
    def connectFile(cls, fileXML):
        cls.filename = fileXML
        
        if not existFile(fileXML):
            cls.createFile(fileXML)
            print(f"Cоздан XML файл {fileXML}")
        
        #получение данных в виде дерева из fileXML файла
        cls.tree = etree.parse(fileXML)
        cls.root = cls.tree.getroot()
        
        return cls
    
    
    @classmethod
    def rewriteFile(cls):
        cls.tree.write(cls.filename, encoding="windows-1251", pretty_print=True )
    
   
    @classmethod
    def createFile(cls, fileXML):    
        xmlData = r"""<extensions>
  <extension type=".MSG">
    <directory type="russ">C:\GitHub\Python\Python-file-assistant-tool\russ</directory>
    <directory type="engl">C:\GitHub\Python\Python-file-assistant-tool\engl</directory>
    <filenames>FOCOMBAT.MSG</filenames>
    <filenames>FOCRAFT.MSG</filenames>
    <filenames>FODLG.MSG</filenames>
    <filenames>FOGAME.MSG</filenames>
    <filenames>FOGM.MSG</filenames>
    <filenames>FOHOLO.MSG</filenames>
    <filenames>FOOBJ.MSG</filenames>
    <filenames>FOTEXT.MSG</filenames>
    <filenames>EXAMPLE.MSG</filenames>
  </extension>
  <extension type=".fos">
    <directory>C:\GitHub\Python\Python-file-assistant-tool\fos</directory>
    <filenames>_defines.fos</filenames>
    <filenames>_dialogs.fos</filenames>
    <filenames>_itempid.fos</filenames>
    <filenames>_msgstr.fos</filenames>
    <filenames>_sample.fos</filenames>
  </extension>
</extensions>"""
        
        #убирает все лишние пробелы и перевод строки
        xmlData = re.sub(r'[\n]+  +|\n', '', xmlData)
        #формируем дерево из строки
        tree = etree.fromstring(xmlData)
        #записываем дерево в файл        
        with open(fileXML, "wb") as f:
            f.write(etree.tostring(tree, encoding="windows-1251", pretty_print=True) )
        

#C:\GitHub\Python\Python-file-assistant-tool\russ\
#C:\GitHub\Python\Python-file-assistant-tool\engl
#C:\GitHub\Python\Python-file-assistant-tool\fos
#нужно ли добавлять в class _XML_?
def _xml_updateDirectories(extensions):
    tagDir = 'directory'
    localizations = {"russ": "русской", "engl": "английской"}
    key = 'type'
    
    pattern = f"Введите путь к дирректории, в которой находятся файлы с расширением "
    for extension in extensions:
        for dir in extension:
            if dir.tag == tagDir:
                text = pattern + extension.attrib[key]
                if dir.attrib:
                    locale = localizations[ dir.attrib[key] ]
                    text += f" в { locale } локализации" 
                text += ':\n'
                dir.text = input(text).strip()
                text = ""
    
    _XML_.rewriteFile()
    print("\nКаталоги изменены")

