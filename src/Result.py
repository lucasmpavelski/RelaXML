from Queriable import Queriable


class Result (Queriable) :
    
    def __init__ (self) :
	self.data = []

    def setData (self, newData) :
	data = newData

    def __getitem__ (self, n) :
	return self.data[n]

    def clone (self, cloneData = True) :
	r = Result()
	r.columns = list(self.columns)
	if (cloneData) :
	    r.data = list(self.data)
	return r

    def _tearColumn (self, line, col) :
	del line[col]
	return line

    def select (self, columns = []) :
	r = self.clone()
	for col in self.columns :
           if col not in columns : 
               map(lambda x : self._tearColumn(x, col), r.data)
	return r

    def orderBy (self, col) :
        self.data.sort(key = (lambda x : x[col]))
	return self

    def where (self, cond) :
	r = self.clone()
	for col in self.columns :
            cond = cond.replace(col, "x['" + col + "']")
	r.data = filter(lambda x : eval(cond), r.data)
	return r

    def join (self, table) :
	r = self.clone(cloneData = False)
	for row1 in self.data :
            for row2 in table.data :
		row = row1
                row.update(row2)
		r.data.append(row)
	return r

    def limit (self, size) :
	return self.limit(0, size)

    def limit (self, lfrom, lto) :
	r = self.clone(cloneData = false)
	r.data = self.data[lfrom:lto]
	return r
