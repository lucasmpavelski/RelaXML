import os
import shutil
import xml.dom.minidom as minidom
from xml.dom.minidom import Document

class Database :

    def __init__ (self, name, location) :
        self.name = name
        self.location = location
        self.path = os.path.join(location, name)
        self.config_path = os.path.join(self.path, "config.xml")
        if (name not in os.listdir(location)) :
            self._write()

    def _save_config (self) :
        config_file = open(self.config_path, 'w')
        self.config_xml.writexml(config_file)
        config_file.close()

    def _write (self) :
        os.mkdir(self.path)
        self.config_xml = Document()

        doc = self.config_xml
        database = doc.createElement("database")
        doc.appendChild(database)
        name = doc.createElement("name")
        nametx = doc.createTextNode(self.name)
        name.appendChild(nametx)
        database.appendChild(name)
        tables = doc.createElement("tables")
        database.appendChild(tables)

        self._save_config()
    
    def drop (self) :
        shutil.rmtree(self.path)

    def createTable (name) :
        pass

    def dropTable (name) :
        pass

    def showTables () :
        pass
