import os
import shutil
import xml.dom.minidom as minidom
from xml.dom.minidom import Document

from Table import Table

class Database :

    def __init__ (self, name, location) :
        """ Starts a Database with name and location. """

        self.name = name
        self.location = location
        self.path = os.path.join(location, name)
        self.config_path = os.path.join(self.path, "config.xml")
        self.tables = {}
        if (name not in os.listdir(location)) : #Search the Database directoty.
            self._write() #If not, create a new Database.
        else :
            self._open() #If found, opens the Database.
    
    def _save_config (self) :
        """ Saves the database configuration in XML. """

        config_file = open(self.config_path, 'w')
        self.config_xml.writexml(config_file)
        config_file.close()
    
    def _write (self) :
        """ Creates a new Database """
        
        os.mkdir(self.path) #Create a directory for the database.
        self.config_xml = Document()
        
        doc = self.config_xml
        database = doc.createElement("database") #Create a node in the database.
        doc.appendChild(database) #XML receives the database.
        
        name = doc.createElement("name") #Create node name.
        nametx = doc.createTextNode(self.name) #Create a new node with text of name.
        name.appendChild(nametx) #Came receives the node created.
        database.appendChild(name) #Database receives name.
        
        self.tables_xml = doc.createElement("tables")
        database.appendChild(self.tables_xml) #Database receives the tables.

        self._save_config()

    def _open (self) :
        """ Opens a existing database. """

        self.config_xml = minidom.parse(self.config_path) #Returns the find XML.
        doc = self.config_xml

        self.name = doc.getElementsByTagName("name")[0].childNodes[0].data #Returns the database name. 

        self.tables_xml = doc.getElementsByTagName("tables")[0] #Returns the node with the tables.
        for table_e in self.tables_xml.childNodes : #Scroll through the tables.
            print table_e.toprettyxml()
            name = table_e.getAttribute("name") #Read name the tables.
            self.tables[name] = Table(name, self.path) #Creates a table object and adds the Hash table.

    def drop (self) :
        """ Deletes the database directory. """

        shutil.rmtree(self.path)

    def createTable (self, name, columns) :
        """ Creates tables on database."""

        doc = self.config_xml

        t = Table(name, self.path)
        t.setColumns(columns)
        self.tables[name] = t

        table_e = doc.createElement("table")
        table_e.setAttribute("name", name)
        self.tables_xml.appendChild(table_e)

        self._save_config()

    def dropTable (self, name) :
        """ Deletes tables. """
        for f in self.tables_xml.childNodes :
            if f.getAttribute("name") == name :
                self.tables_xml.removeChild(f)

        os.remove(self.tables[name].path)
        del self.tables[name]

    def showTables (self) :
        """ Shows existing tables. """

        r = ""
        for name in self.tables.keys() : #Scroll through the tables.
            r = r + name + "\n"
        return r

    def insertInto (self, tb_name, values) :
        self.tables[tb_name].insert(values)


    def fromTables (self, tables) :
	r = Result()
	for t in tables :
	   r.join(t)
	return r
