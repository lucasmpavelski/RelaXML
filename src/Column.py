
class Column :
    def __init__ (self, name, type) :
        self.name = name
	self.type = type

    def like (self, obj) :
	return type(obj).__name__ == self.type
