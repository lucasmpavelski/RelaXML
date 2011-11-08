import os
import xml.dom.minidom as minidom
from xml.dom.minidom import Document
from threading import Timer

from Result import Result
from Column import Column


class ValueTypeExeption (Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class ColumnExeption (Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class Table (Result) :

    def __init__ (self, name, location) :
        super(Table, self).__init__()
        self.name = name
        self.location = location
        self.path = os.path.join(location, name + ".xml")
        self.columns = []
        self.col_names = []

        self.life = Timer(10, self._kill)

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
        self._live()
        doc = self.xml

        self.name = doc.getElementsByTagName("name")[0].childNodes[0].data #Returns the table name. 

        self.columns_xml = doc.getElementsByTagName("columns")[0]#Returns the node with the columns.
        self.col_n = len(self.columns_xml.childNodes)
        self.columns = [None] * self.col_n

        for col_e in self.columns_xml.childNodes : #Scroll through the columns.
            i = col_e.getAttribute("id")
            name = col_e.getAttribute("name") #Read name the columns.
            typen = col_e.getAttribute("type") #Read the type the columns.

            self.columns[i] = Column(name, typen)

    def setColumns (self, columns) :
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
        self.xml = minidom.parse(self.path)
        self.data_xml = self.xml.getElementsByTagName("data")[0]

    def _kill (self) :
        del self.data_xml
        del self.xml

    def desc (self) :
        """ Show table config. """

        r = "Table: " + self.name + "\n"
        for name, col in self.columns.iteritems() : #Scroll through the columns.
            r = r + "Column: " + name + " (" + col.typeName + ")\n"
        return r

    def _column(self, name) :
        col = filter(lambda (x) : x.name == name, self.columns)
        if col == [] : 
            return None 
        else :
            return col[0]

    def insert (self, values) :
        cols = self.columns
        new_row = {}

        if type(values) is dict :
            new_row = values

            for cnm, cval in values.iteritems() :
                if cnm not in self.col_names :
                    raise ColumnExeption("No column named " + cnm)
                elif not self._column(cnm).like(cval) :
                    raise ValueTypeExeption("Wrong type for " + cnm)

                new_row[cnm] = cval

            for c in cols :
                if c.name not in new_row.keys() :
                    new_row[c.name] = ""
        else :
            raise TypeException("Insert values type error.")

        self.data.append(new_row)

        row = self.xml.createElement("row")
        for col, v in new_row.iteritems() :
            row.setAttribute(self.columns[col].ns_name, str(v))
        self.data_xml.appendChild(row)

        self._save_xml()
