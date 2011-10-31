import unittest

from Column import Column

class TestColumn (unittest.TestCase) :
    
    def testLike (self) :
	c = Column("name", int)
	assertTrue(c.like(345))
	c = Column("name", str)
	s = "nha"
	assertTrue(c.like(s))
	assertTrue(Column("asdf", complex).like(5j+3))


if __name__ == "__main__" :
    unittest.main()
