from Queriable import Queriable



class Result (Queriable) :
    
    def __init__ (self) :
	self.data = []

    def setData (self, newData) :
	data = newData

    def __getitem__ (self, n) :
	return self.data[n]

    def _tearColumn (self, line, col) :
	del line[col]
	return line

    def select (self, columns = []) :
	r = Result()
	r.data = list(self.data)
	r.columns = columns
        for col in self.columns :
           if col not in columns : 
               map(lambda x : self._tearColumn(x, col), r.data)
	return r

    def orderBy (self, col) :
        self.data.sort(key = (lambda x : x[col]))
	return self

    def where (self, cond) :
	r = Result()
	r.data = list(self.data)
	r.columns = self.columns
	for col in self.columns :
            cond = cond.replace(col, "x['" + col + "']")
	r.data = filter(lambda x : eval(cond), r.data)
	return r
