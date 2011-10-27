
class Result (Queryable) :
    
    def __init__ (self) :
	pass

    def setData (self, newData) :
	data = newData

    def __getter__ (self, n) :
	self.data[n]
