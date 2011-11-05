import unittest
import os
import shutil
import xml.dom.minidom as minidom

from DBMS import DBMS

class TestTable (unittest.TestCase) :

    def setUp (self) :
        self.path = 'test/dump'
        os.mkdir(self.path)
        self.name = 'dbms_test'
        self.d = DBMS(self.name, self.path)
        self.database_name = "database_test"
        self.d.createDatabase(self.database_name)
        self.database = self.d.useDatabase(self.database_name)

    def tearDown (self) :
        pass
        self.d.clear()
        shutil.rmtree(self.path)

    def testTableFileCreation (self) :
        self.database.createTable("test_f", {})
        t = self.database.tables["test_f"]

        t_xml = minidom.parse(t.path)
        self.assertTrue("<name>test_f</name>" in t_xml.toxml(), "Table has not created name element properly")
        self.assertTrue("<data/>" in t_xml.toxml(), "Table has not created an empty data element")
        
        self.database.dropTable("test_f")
        path = self.database.path
        self.assertFalse("test_f.xml" in os.listdir(path), "Database did not destroy the table file on drop")
 
    def testColumnElements (self) :
        columns = {'name': 'str', 'a_number': 'int', 'a great number': 'complex'}
        self.database.createTable("test_col", columns)
        t = self.database.tables["test_col"]

        t_xml = minidom.parse(t.path)
        self.assertTrue('<column name="name" type="str"/>' in t_xml.toxml(), "Table has not appended string column in the file")
        self.assertTrue('<column name="a great number" type="complex"/>' in t_xml.toxml(), "Table has not appended complex column in the file")

    def testLoading (self) :
        columns = {'name': 'str', 'a_number': 'int', 'a great number': 'complex'}
        self.database.createTable("test_col", columns)
        t = self.database.tables["test_col"]

        self.assertTrue('a_number' in t.desc(), "Table has not loaded the columns properly.")

    def testInsertion (self) :
        columns = {'name': 'str', 'a_number': 'int', 'a great number': 'complex'}
        self.database.createTable("test_col", columns)
        t = self.database.tables["test_col"]

        t.insert(["asdf", 5, 5j])

        print t.xml.toxml()
        self.assertTrue('<row a_great_number="5j" a_number="asdf" name="5"/>' in t.xml.toxml(), "Table has not inserted the values on the xml properly.")

if __name__ == "__main__" :
    unittest.main()
