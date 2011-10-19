import unittest
import os
import shutil
import xml.dom.minidom as minidom

from DBMS import DBMS

class TestDBMS (unittest.TestCase) :

    def setUp (self) :
        self.path = 'test/dump'
        os.mkdir(self.path)
        self.name = 'dbms_test'

    def tearDown (self) :
        shutil.rmtree(self.path)

    def testCreateClear (self) :
        self.d = DBMS(self.name, self.path)

        self.assertTrue(self.name in os.listdir(self.d.location), "DBMS has not created the dir")
   
        self.assertTrue("config.xml" in os.listdir(self.d.path), "DBMS has not created the config file")
        f = open(self.d.config_path)
        doc = minidom.parse(f)
        self.assertTrue(("<databases") in doc.toxml(), "DBMS has not write in the config file")
   
        del doc
        self.d.clear()
        self.assertFalse(self.d.name in os.listdir(self.d.location), "DBMS has not destroyed the dir")
   
    def testOpen (self) :
        d = DBMS(self.name, self.path)
        d.createDatabase("nha")
        d.createDatabase("asdf")
        names = d.databases.keys()
        del d

        d = DBMS(self.name, self.path)
        self.assertEqual(names, d.databases.keys(), "DBMS has not open config file properly")

        d.clear()
   
    def testCreateDropDatabase (self) :
        self.d = DBMS(self.name, self.path)

        self.d.createDatabase("nha")
        self.assertTrue("nha" in os.listdir(self.d.path), "DBMS has not created the database dir")
        self.assertTrue("nha" in self.d.showDatabases(), "DBMS has not created the database")
        self.d.dropDatabase("nha")
        self.assertFalse("nha" in os.listdir(self.d.path), "DBMS has not destroyed the database dir")
        self.assertFalse("nha" in self.d.showDatabases(), "DBMS has not dropped the database")
   
        self.d.clear()

if __name__ == "__main__" :
    unittest.main()
