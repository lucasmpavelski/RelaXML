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
        self.database = d.useDatabase(self.database_name)

    def tearDown (self) :
        self.d.clear()
        shutil.rmtree(self.path)

    def testTableFileCreation (self) :
        self.database.createTable("test_f", {})
        t = d.tables["test_f"]
        
        t_xml = minidom.parse(t.path)
        self.assertTrue("<name>test_cf</name>" in t_xml.toxml(), "Table has not created name element properly")
        self.assertTrue("<data/>" in t_xml.toxml(), "Table has not created an empty data element")
        
        self.database.dropTable("test_f")
        path = self.database.path
        self.assertFalse("test_f" not in os.listdir(path), "Database did not destroy the table file on drop")
 
    def testColumnElements (self) :
        columns = {'name': str, 'a_number': int, 'a great number': complex}
        d.createTable("test_col", columns)

        t_xml = minidom.parse(t.path)
        self.assertTrue('<name>name</name><type>str</type>' in t_xml.toxml(), "Table has not appended string column in the file")
         self.assertTrue('<name>a great number</name><type>complex</type>' in t_xml.toxml(), "Table has not appended complex column in the file")


if __name__ == "__main__" :
    unittest.main()
