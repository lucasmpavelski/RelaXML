import os
import shutil

from Database import Database

class DBMS :

    def __init__ (self, name, location = ".") :
        self.name = name
        self.location = location
        self.path = os.path.join(location, name)
        if (name not in os.listdir(location)) :
            self._write()

    def _write (self) :
        os.mkdir(self.path)
        self.databases = {}
    
    def clear (self) :
        shutil.rmtree(self.path)

    def createDatabase (self, name) :
        d = Database(name, self.path)
        self.databases[name] = d

    def dropDatabase (self, name) :
        self.databases[name].drop()
        del self.databases[name]
