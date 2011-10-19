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

    def testTableFile (self) :
	d.createTable("test_f")
	t = d.tables["test_f"]

	t_xml = minidom.parse(t.path)
        self.assertTrue("<name>test_cf</name>" in cf.toxml(), "Database has not created config file properly")
        self.assertTrue("<data/>" in cf.toxml(), "Database has not created config file properly")

if __name__ == "__main__" :
    unittest.main()
