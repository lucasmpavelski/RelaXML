
class Result (Queryable) :
    
    def __init__ (self) :
	self.data = []

    def setData (self, newData) :
	data = newData

    def __getter__ (self, n) :
	self.data[n]

    def _tearColumn (line, col) :
	pass

    def select (columns = []) :
	for col in self.columns :
            if col not in columns : 
		map(lambda x : del x[col], self.data)


