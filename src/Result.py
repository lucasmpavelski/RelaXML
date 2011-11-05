from Queriable import Queriable



class Result (Queriable) :
    
    def __init__ (self) :
	self.data = []

    def setData (self, newData) :
	data = newData

    def __getitem__ (self, n) :
	return self.data[n]

    def _tearColumn (line, col) :
	pass

    def select (columns = []) :
        pass
        # for col in self.columns :
            #if col not in columns : 
		#map(lambda x : del x[col], self.data)


