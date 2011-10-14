
class Queriable :
    def __init__ (self) :
        pass
    
    def select (columns) :
        pass
        
    def fromTables (tables) :
        pass 
        
    def where (condition) :
        pass
        
    def orderBy (column) :
        pass

class Data :
    
    def __init__ (self, name) :
        self.name = name
        if type(name) is int :
            print "name is integer!!", name
            
t = Table("asdf")
t = Table(5)
