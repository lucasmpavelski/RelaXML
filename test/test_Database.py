import unittest
import os
import shutil
import xml.dom.minidom as minidom

from DBMS import DBMS

class TestDatabase (unittest.TestCase) :

    def setUp (self) :
        self.path = 'test/dump'
        os.mkdir(self.path)
        self.name = 'dbms_test'
        self.d = DBMS(self.name, self.path)

    def tearDown (self) :
        self.d.clear()
        shutil.rmtree(self.path)

    def testOpenUseDatabase (self) :
        self.d.createDatabase("test")
	del self.d

	self.d = DBMS(self.name, self.path)

        db = self.d.useDatabase("test")
        self.assertEqual(db.name, "test", "DBMS has not returned database correctly")

    def testConfigFile (self) :
        self.d.createDatabase("test_cf")
        db = self.d.useDatabase("test_cf")
        cf = minidom.parse(db.config_path)

        self.assertTrue("<name>test_cf</name>" in cf.toxml(), "Database has not created config file properly")
        self.assertTrue("<tables/>" in cf.toxml(), "Database has not created config file properly")

        self.d.dropDatabase("test_cf")

    def testCreateDropTable (self) :
        self.d.createDatabase('test_ct')
        db = self.d.useDatabase('test_ct')

        db.createTable("testtable", {})
        self.assertTrue("testtable" in db.showTables(), "Database has not created the table")
        db.dropTable("testtable")
        self.assertTrue("testtable" not in db.showTables(), "Database has not dropped the table")

if __name__ == "__main__" :
    unittest.main()
