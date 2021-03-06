

class Result(object) :
    
    def __init__ (self) :
	""" Returns the results of queries. """
        self.data = []
        self.col_names = []

    def __getitem__ (self, n) :
	""" Gets a row of data. """
	return self.data[n]

    def clone (self, cloneData = True) :
	""" Clones results. """
	r = Result()
	r.col_names = list(self.col_names)
	if (cloneData) :
            r.data = []
            for i, row in enumerate(self.data) :
	       r.data.append(dict(self.data[i]))
	return r

    def _tearColumns (self, line, cols) :
        for col in cols :
	    del line[col]
	return line

    def select (self, columns = []) :
	""" Selects a column from table. """
	r = self.clone()
        if columns != [] :
          rem_cols = list(set(self.col_names) - set(columns))
          self.col_names = list(set(columns) - set(self.col_names))
          map(lambda x : self._tearColumns(x, rem_cols), r.data)
	return r

    def orderBy (self, col) :
	""" Sort a column. """
	r = self.clone()
        r.data.sort(key = (lambda x : x[col]))
	return r

    def where (self, cond) :
	""" Condition required. """
	r = self.clone()
	for col in self.col_names :
            cond = cond.replace(col, "x['" + col + "']")
	r.data = filter(lambda x : eval(cond), r.data)
	return r

    def join (self, table) :
	""" Makes the Cartesian product between the rows of the table. """
        if self.data == [] :
            return table.clone()
        elif table.data == [] :
            return self.clone()

	r = self.clone(cloneData = False)
	for row1 in self.data :
            for row2 in table.data :
		row = row1
                row.update(row2)
                r.data.append(row)

        r.col_names = self.col_names
        r.col_names.extend(table.col_names)

	return r

    def limit (self, size) :
	""" Returns a number (size) of the results of table. """
	return self.limit(0, size)

    def limit (self, lfrom, lto) :
	""" Returns a number (range lfrom and lto) of the results of table. """
	r = self.clone(cloneData = false)
	r.data = self.data[lfrom:lto]
        return r

    def min_value (self, col) :
        if self.data :
           return min(self.data, key = lambda x : x[col])[col]
        else :
           return 0

    def max_value (self, col) :
        if self.data :
           return max(self.data, key = lambda x : x[col])[col]
        else :
           return 0
