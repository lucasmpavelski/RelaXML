import os
import shutil
import xml.dom.minidom as minidom
from xml.dom.minidom import Document

from Database import Database

class DatabaseAlreadyExistError :
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "Database " + name + " already exists."
     

class DBMS :

    def __init__ (self, name, location = ".") :
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
        config_file = open(self.config_path, 'w')
        self.config_xml.writexml(config_file)
        config_file.close()

    def _write (self) :
        os.mkdir(self.path)
        self.config_xml = Document()

        doc = self.config_xml
        dbms = doc.createElement("dbms")
        doc.appendChild(dbms)
        self.databases_xml = doc.createElement("databases")
        dbms.appendChild(self.databases_xml)

        self._save_config()

    def _open (self) :
        self.config_xml = minidom.parse(self.config_path)
        self.databases_xml = self.config_xml.getElementsByTagName("databases")[0]

        dbs = self.databases_xml.childNodes
        for db in dbs :
            name = db.getAttribute("name")
            self.databases[name] = Database(name, self.path)
    
    def clear (self) :
        shutil.rmtree(self.path)

    def createDatabase (self, name) :
        if (name in self.databases.keys()) :
            raise DatabaseAlreadyExistError(name)
        d = Database(name, self.path)
        self.databases[name] = d

        db = self.config_xml.createElement("database")
        db.setAttribute("name", name)
        self.databases_xml.appendChild(db)

        self._save_config()

    def dropDatabase (self, name) :
        self.databases[name].drop()
        del self.databases[name]

    def showDatabases (self) :
        r = ""
        for name in self.databases.keys() :
            r = r + name + "\n"
        return r

    def useDatabase (self, name) :
        d = self.databases[name]
        return d

    def useConcurrentDatabase (self, name) :
        d = self.useDatabase(name)
        d.threadSafeInit()
        return d
