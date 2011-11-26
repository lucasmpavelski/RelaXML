import os
import xml.dom.minidom as minidom
from xml.dom.minidom import Document
from threading import Timer

from Result import Result
from Column import Column


class Table (Result) :

    def __init__ (self, name, location) :
	""" Initiates the tables. """
        super(Table, self).__init__()
        self.name = name
        self.location = location
        self.path = os.path.join(location, name + ".xml")
        self.columns = []
        self.alive = False

        if (name + ".xml" not in os.listdir(location)) : #Finds a table on database directory.
            self._write() #If not, Creates a new tables.
        else :
            self._open() #If found, opens the tables.

    def _save_xml (self) :
        """ Saves the tables configuration on XML. """

        file = open(self.path, 'w')
        self.xml.writexml(file)
        file.close()

    def _write (self) :
        """ Creates a new table. """

        self.xml = Document()

        doc = self.xml
        table = doc.createElement("table") #Creates a node in the table.
        doc.appendChild(table) #XML receives the table.

        name = doc.createElement("name") #Create node name.
        nametx = doc.createTextNode(self.name) #Create a new node with text of name.
        name.appendChild(nametx) #Name receives the node created.
        table.appendChild(name) #Table receives name.

        self.columns_xml = doc.createElement("columns")
        table.appendChild(self.columns_xml) #Table receives the columns.

        self.data_xml = doc.createElement("data")
        table.appendChild(self.data_xml) #table receives the data.

        self._save_xml()

    def _open (self) :
        """ Opens a existing table. """
        self.xml = minidom.parse(self.path)
        doc = self.xml

        self.name = doc.getElementsByTagName("name")[0].childNodes[0].data #Returns the table name. 

        self.columns_xml = doc.getElementsByTagName("columns")[0]#Returns the node with the columns.
        self.col_n = len(self.columns_xml.childNodes)
        self.columns = [None] * self.col_n
        self.col_names = [None] * self.col_n

        for col_e in self.columns_xml.childNodes : #Scroll through the columns.
            i = col_e.getAttribute("id")
            name = col_e.getAttribute("name") #Read name the columns.
            typen = col_e.getAttribute("type") #Read the type the columns.

            self.columns[int(i)] = Column(name, typen)
            self.col_names[int(i)] = name

        self._live()

    def _validateColumnName (self, name) :
	""" Checks if the field name is unique. """
        for cname in self.col_names :
            if name in cname or cname in name :
                raise Exception("The name " + name + " conficts with" + 
                  " the existing name " + cname + ".")

    def _validateColumnType (self, type_name):
	""" Checks if the field Type is valid. """
        if type_name not in ['int', 'str', 'float', 'long', 'complex',
                             'type'] :
            raise Exception("The type " + type_name + " is not allowed.")

    def setColumns (self, columns) :
	""" Initiates the columns from table. """
        for name, type_name in columns.iteritems() :
            self._validateColumnName(name)
            self._validateColumnType(type_name)

        for name, type_name in columns.iteritems() :
            self.columns.append(Column(name, type_name))
        self.col_n = len(columns)
        self.col_names = columns.keys()

        doc = self.xml
        for i, col in enumerate(self.columns) :
            col_el = doc.createElement("column")
            col_el.setAttribute("id", str(i))
            col_el.setAttribute("name", col.name)
            col_el.setAttribute("type", col.typeName)
            self.columns_xml.appendChild(col_el)
        self._save_xml()

    def _live (self) :
	""" Reloads a dead table. """
        if not self.alive :
            self.xml = minidom.parse(self.path)
            self.data_xml = self.xml.getElementsByTagName("data")[0]

            self.data = []
            for i, row_e in enumerate(self.data_xml.childNodes) :
                row = {}
                for col in self.columns :
                    k = col.name
                    v = col.valueOf(row_e.getAttribute(col.ns_name))
                    row[k] = v
                self.data.append(row)
            self.alive = True
        else :
            self.life.cancel()

        self.life = Timer(20, self._kill)
        self.life.start()

    def _kill (self) :
	""" Kill  the table and frees memory. """
        del self.data_xml
        del self.xml
        del self.data
        self.alive = False

    def desc (self) :
        """ Show table config. """

        r = "Table: " + self.name + "\n"
        for name, col in self.columns.iteritems() : #Scroll through the columns.
            r = r + "Column: " + name + " (" + col.typeName + ")\n"
        return r

    def _column(self, name) :
	""" Add name to the column. """
        col = filter(lambda (x) : x.name == name, self.columns)
        if col == [] : 
            return None 
        else :
            return col[0]

    def insert (self, values) :
	""" Insert values in the tables. """
        cols = self.columns
        new_row = {}

        if type(values) is dict :
            new_row = values

            for cnm, cval in values.iteritems() :
                if cnm not in self.col_names :
                    raise Exception("No column named " + cnm)
                elif not self._column(cnm).like(cval) :
                    raise Exception("Wrong type for " + cnm)

                new_row[cnm] = cval

            for c in cols :
                if c.name not in new_row.keys() :
                    new_row[c.name] = ""
        else :
            raise Exception("Insert values type error. Got " +
                type(values).__name__ + " instead of dict.")

        self.data.append(new_row)

        row = self.xml.createElement("row")
        for col, v in new_row.iteritems() :
            row.setAttribute(self._column(col).ns_name, str(v))
        self.data_xml.appendChild(row)

        self._save_xml()

    def deleteRows (self, rows) :
	""" Deletes in the table, memory and XML. """
        for i, r in enumerate(self.data) :
            if r in rows :
                del self.data[i]

        for row_e in self.data_xml.childNodes :
            row = {}
            for col in self.columns :
                v = row_e.getAttribute(col.ns_name)
                row[col.name] = col.valueOf(v)
            if row in rows :
                self.data_xml.removeChild(row_e)

        self._save_xml()
