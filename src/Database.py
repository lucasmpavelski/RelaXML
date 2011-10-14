import os
import shutil

class Database :

    def __init__ (self, name, location) :
        self.name = name
        self.location = location
        self.path = os.path.join(location, name)
        print location, self.path
        if (name not in os.listdir(location)) :
            self._write()

    def _write (self) :
        os.mkdir(self.path)
    
    def drop (self) :
        shutil.rmtree(self.path)
