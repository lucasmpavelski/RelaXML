import unittest
import os

from DBMS import DBMS

class TestDBMS (unittest.TestCase) :

  def testCreateClear (self) :
      path = '/tmp'
      name = 'name'

      d = DBMS(name, path)
      self.assertTrue(d.name in os.listdir(d.location), "DBMS has not created the dir")
      d.clear()
      self.assertFalse(d.name in os.listdir(d.location), "DBMS has not destroyed the dir")

  def testCreateDatabase (self) :
      path = '/tmp'
      name = 'name'

      d = DBMS(name, path)

      d.createDatabase("nha")
      self.assertTrue("nha" in os.listdir(d.path), "DBMS has not created the database dir")
      d.dropDatabase("nha")
      self.assertFalse("nha" in os.listdir(d.path), "DBMS has not destroyed the database dir")

      d.clear()

if __name__ == "__main__" :
    unittest.main()
