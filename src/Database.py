import os
import shutil
import xml.dom.minidom as minidom
from xml.dom.minidom import Document

from Table import Table

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
        database.appendChild(self.tables_xml)

        self._save_config()

    def _open (self) :
	self.config_xml = minidom.parse(self.config_path)
	doc = self.config_xml

	self.name = doc.getElementsByTagName("name")[0].childNodes[0].data

        self.tables_xml = doc.getElementsByTagName("tables")[0]
	for table_e in self.tables_xml.childNodes :
	    print table_e.toprettyxml()
	    name = table_e.getAttribute("name")
	    self.tables[name] = Table(name, self.path)

    def drop (self) :
        shutil.rmtree(self.path)

    def createTable (self, name, columns) :
        doc = self.config_xml

	t = Table(name, self.path)
	t.setColumns(columns)
        self.tables[name] = t

	table_e = doc.createElement("table")
	table_e.setAttribute("name", name)
	self.tables_xml.appendChild(table_e)

	self._save_config()

    def dropTable (name) :
	del self.tables[name]

    def showTables () :
        r = ""
        for name in self.tables.keys() :
		r = r + name + "\n"
