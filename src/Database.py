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
	self.tables = {}
        if (name not in os.listdir(location)) :
            self._write()
	else :
	    self._open()

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

        self.tables_xml = doc.createElement("tables")
        database.appendChild(tables_xml)

        self._save_config()

    def _open (self) :
	self.config_xml = minidom.parse(self.path)
	doc = self.confin_xml

	self.name = doc.getElementsByTagName("name")[0].childNodes[0].data

        self.tables_xml = doc.getElementsByTagName("tables")[0]
	for table_e in self.tables_xml.childNodes :
	    name = table_e.getElementsByTagName("name")[0].childNodes[0].data
	    self.tables[name] = Table(name, self.path)
    
    def drop (self) :
        shutil.rmtree(self.path)

    def createTable (name) :
        doc = self.config_xml
        self.tables[name] = Table(name, self.path)

	table_e = doc.createElement("name")
	table_e_nametx = doc.createTextNode(name)
	table_e.appendChild(table_e_nametx)

	self.tables_xml.appendChild(table_e)

    def dropTable (name) :
	del self.tables[name]

    def showTables () :
        r = ""
        for name in self.tables.keys() :
        r = r + name + "\n"
