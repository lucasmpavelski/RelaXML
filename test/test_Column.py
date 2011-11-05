import unittest

from Column import Column

class TestColumn (unittest.TestCase) :
    
    def testLike (self) :
	c = Column("name", 'int')
	self.assertTrue(c.like(345))
	c = Column("name", 'str')
	s = "nha"
        self.assertTrue(c.like(s))
        self.assertTrue(Column("asdf", 'complex').like(5j+3))


if __name__ == "__main__" :
    unittest.main()
