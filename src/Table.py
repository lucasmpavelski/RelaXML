import os
import xml.dom.minidom as minidom
from xml.dom.minidom import Document

from Column import Column


class Table :

    def __init__ (self, name, location) :
        self.name = name
        self.location = location
	self.path = os.path.join(location, name + ".xml")
	self.columns = {}
        if (name + ".xml" not in os.listdir(location)) :
            self._write()
	else :
	    self._open()

    def _save_xml (self) :
        file = open(self.path, 'w')
        self.xml.writexml(file)
        file.close()

    def _write (self) :
        self.xml = Document()

        doc = self.xml
        table = doc.createElement("table")
        doc.appendChild(table)

        name = doc.createElement("name")
        nametx = doc.createTextNode(self.name)
        name.appendChild(nametx)
        table.appendChild(name)

	self.columns_xml = doc.createElement("columns")
	table.appendChild(self.columns_xml)
	
        self.data_xml = doc.createElement("data")
        table.appendChild(self.data_xml)

        self._save_xml()
    
    def _open (self) :
	self._live()
	doc = self.xml

	self.name = doc.getElementsByTagName("name")[0].childNodes[0].data

	self.columns_xml = doc.getElementsByTagName("columns")[0]
	for col_e in self.columns_xml.childNodes :
	    name = col_e.getAttribute("name")
	    type = col_e.getAttribute("type")

	    self.columns[name] = Column(name, type)

    def setColumns (self, columns) :
	self.columns = columns

	doc = self.xml
	for col_name, col_type in self.columns.iteritems() :
	    col_el = doc.createElement("column")
	    col_el.setAttribute("name", col_name)
	    col_el.setAttribute("type", col_type)
	    self.columns_xml.appendChild(col_el)
	self._save_xml()

    def _live (self) :
        self.xml = minidom.parse(self.path)
	self.data_xml = self.xml.getElementsByTagName("data")[0]

    def _kill (self) :
	del self.data_xml
	del self.xml
