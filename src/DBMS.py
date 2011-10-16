import os
import shutil
import xml.dom.minidom as minidom
from xml.dom.minidom import Document

from Database import Database

class DBMS :

    def __init__ (self, name, location = ".") :
        self.name = name
        self.location = location
        self.path = os.path.join(location, name)
        self.databases = {}
        print name, os.listdir(location)
        if (name not in os.listdir(location)) :
            self._write()
        else :
            self._open()
            print 'opened'

    def _save_config (self) :
        config_file = open(self.config_path, 'w')
        self.config_xml.writexml(config_file)
        config_file.close()

    def _write (self) :
        os.mkdir(self.path)
        self.config_path = os.path.join(self.path, 'config.xml')
        self.config_xml = Document()

        doc = self.config_xml
        dbms = doc.createElement("dbms")
        doc.appendChild(dbms)
        databases = doc.createElement("databases")
        dbms.appendChild(databases)

        self._save_config()

    def _open (self) :
        self.config_path = os.path.join(self.path, 'config.xml')
        self.config_xml = minidom.parse(self.config_path)
        print self.config_xml.toxml()

        names = self.config_xml.getElementsByTagName("databases")[0].childNodes
        for nm in names :
            name = nm.childNodes[0].data
            self.databases[name] = Database(name, self.path)
    
    def clear (self) :
        shutil.rmtree(self.path)

    def createDatabase (self, name) :
        d = Database(name, self.path)
        self.databases[name] = d

        databases = self.config_xml.getElementsByTagName("databases")[0]
        db_name = self.config_xml.createElement("name")
        nametx = self.config_xml.createTextNode(name)
        db_name.appendChild(nametx)
        databases.appendChild(db_name)

        self._save_config()

    def dropDatabase (self, name) :
        self.databases[name].drop()
        del self.databases[name]

    def showDatabases (self) :
        for db in self.databases :
            print db
