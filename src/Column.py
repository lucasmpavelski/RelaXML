
class Column :
    def __init__ (self, name, theType) :
        self.name = name
        self.ns_name = name.replace(" ", "_")
	self.typeName = theType

    def like (self, obj) :
        return type(obj).__name__ == self.typeName

    def valueOf (self, objstr) :
	return eval(self.typeName)(objstr)
