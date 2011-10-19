import os
import xml.dom.minidom as minidom
from xml.dom.minidom import Document

class Table :

    def __init__ (self, name, location) :
        self.name = name
        self.location = location
	self.path = os.path.join(location, name + ".xml")
        if (name not in os.listdir(location)) :
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
        doc.appendChild(database)
        name = doc.createElement("name")
        nametx = doc.createTextNode(self.name)
        name.appendChild(nametx)
        table.appendChild(name)
        data = doc.createElement("data")
        database.appendChild(data)

        self._save_xml()
    
    def _open (self) :
	pass

    def _live (self) :
        pass

    def _kill (self) :
	pass
