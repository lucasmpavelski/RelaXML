import unittest
import os
import shutil
import xml.dom.minidom as minidom

from Result import Result


class TestTable (unittest.TestCase) :

    def test_All (self) :
        r = Result()
        r.name = "tab1"
        r.columns = ["col1", "col2"]
        r.data = data
        print r.orderBy("col2").data
        print r.orderBy("col1").data
        print r.where("col1 == 45").data

        data2 = [{"col3":43, "col4":1 },
                 {"col3":15, "col4":41},
                 {"col3":77, "col4":87},
                 {"col3":04, "col4":4 },
                 {"col3":07, "col4":8 },
                 {"col3":54, "col4":8 }]
        r2 = Result()
        r2.columns = ["col3", "col4"]
        r2.data = data2

        r1 = Result()
        r1.columns = ["c1", "c2"]
        r1.data = [{"c1": "c1v1", "c2": "c2v1"},
                   {"c1": "c1v2", "c2": "c2v2"}]

        r2 = Result()
        r2.columns = ["2c1", "2c2"]
        r2.data = [{"2c1": "c1v1", "2c2": "c2v1"},
                   {"2c1": "c1v2", "2c2": "c2v2"}]

        for row in r1.join(r2).where("2c2 == c2").data :
            print row
