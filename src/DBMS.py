import os
import shutil
import xml.dom.minidom as minidom
from xml.dom.minidom import Document

from Database import Database

class DatabaseNotFoundException (Exception) :
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "No database with name " + self.name + "."
     

class DBMS :

    def __init__ (self, name, location = ".") :
	""" Initiates the database manager. """
        self.name = name
        self.location = location
        self.path = os.path.join(location, name)
        self.config_path = os.path.join(self.path, 'config.xml')
        self.databases = {}
        if (name not in os.listdir(location)) :
            self._write()
        else :
            self._open()

    def _save_config (self) :
	""" Saves the settings of database manager. """
        config_file = open(self.config_path, 'w')
        self.config_xml.writexml(config_file)
        config_file.close()

    def _write (self) :
	""" Writes the XML of the database manager. """
        os.mkdir(self.path)
        self.config_xml = Document()

        doc = self.config_xml
        dbms = doc.createElement("dbms")
        doc.appendChild(dbms)
        self.databases_xml = doc.createElement("databases")
        dbms.appendChild(self.databases_xml)

        self._save_config()

    def _open (self) :
	""" Opens the database manager. """

        self.config_xml = minidom.parse(self.config_path)
        self.databases_xml = self.config_xml.getElementsByTagName("databases")[0]

        dbs = self.databases_xml.childNodes
        for db in dbs :
            name = db.getAttribute("name")
            self.databases[name] = Database(name, self.path)
    
    def clear (self) :
	""" Deletes the setting of the database manager. """

        shutil.rmtree(self.path)

    def createDatabase (self, name) :
	""" Creates a new database. """
        if (name in self.databases.keys()) :
            raise Exception("The database " + name + " already exists.")
        d = Database(name, self.path)
        self.databases[name] = d

        db = self.config_xml.createElement("database")
        db.setAttribute("name", name)
        self.databases_xml.appendChild(db)

        self._save_config()

    def dropDatabase (self, name) :
	""" Deletes the desired database. """
        if name not in self.databases.keys() :
            raise DatabaseNotFoundException(name)
        self.databases[name].drop()
        del self.databases[name]

    def showDatabases (self) :
	""" Shows all existing databases. """
        r = ""
        for name in self.databases.keys() :
            r = r + name + "\n"
        return r

    def useDatabase (self, name) :
        if (name not in self.databases.keys()) :
            raise DatabaseNotFoundException(name)
	""" Uses the desired database. """
        d = self.databases[name]
        return d

    def useConcurrentDatabase (self, name) :
	""" Uses the database with concurrent control. """
        d = self.useDatabase(name)
        d.threadSafeInit()
        return d
