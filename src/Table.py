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
        if (name + ".xml" not in os.listdir(location)) : #Finds a table on database directory.
            self._write() #If not, Creates a new tables.
	else :
	    self._open() #If found, opens the tables.

    def _save_xml (self) :
    """ Saves the tables configuration on XML. """
    
        file = open(self.path, 'w')
        self.xml.writexml(file)
        file.close()

    def _write (self) :
    """ Creates a new table. """
    
        self.xml = Document()

        doc = self.xml
        table = doc.createElement("table") #Creates a node in the table.
        doc.appendChild(table) #XML receives the table.

        name = doc.createElement("name") #Create node name.
        nametx = doc.createTextNode(self.name) #Create a new node with text of name.
        name.appendChild(nametx) #Name receives the node created.
        table.appendChild(name) #Table receives name.

	self.columns_xml = doc.createElement("columns")
	table.appendChild(self.columns_xml) #Table receives the columns.
	
        self.data_xml = doc.createElement("data")
        table.appendChild(self.data_xml) #table receives the data.

        self._save_xml()
    
    def _open (self) :
    """ Opens a existing table. """
	self._live()
	doc = self.xml

	self.name = doc.getElementsByTagName("name")[0].childNodes[0].data #Returns the table name. 

	self.columns_xml = doc.getElementsByTagName("columns")[0]#Returns the node with the columns.
	for col_e in self.columns_xml.childNodes : #Scroll through the columns.
	    name = col_e.getAttribute("name") #Read name the columns.
	    type = col_e.getAttribute("type") #Read the type the columns.

	    self.columns[name] = Column(name, type) #Creates a table object and adds the Hash columns.

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
