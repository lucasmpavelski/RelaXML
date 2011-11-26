import os

from DBMS import DBMS

def createEx () :
    dbms = DBMS('example', '.')
    dbms.createDatabase("db_example")
    db = dbms.useDatabase("db_example")
    columns1 = {"t1id" : "int", "t1name" : "str", "t1phone" : "str"}
    db.createTable("table1_ex", columns1)
    columns2 = {"t2id" : "int", "t2name" : "str", "t2phone" : "str"}
    db.createTable("table2_ex", columns2)

def populate (db) :
    db.insertInto("table1_ex", {"t1id": 0, "t1name": "joao", "t1phone": "6548-9874"})
    db.insertInto("table1_ex", {"t1id": 1, "t1name": "jose", "t1phone": "6548-1513"})
    db.insertInto("table1_ex", {"t1id": 2, "t1name": "jair", "t1phone": "4879-9899"})
    db.insertInto("table1_ex", {"t1id": 3, "t1name": "jura", "t1phone": "7897-1111"})

    db.insertInto("table2_ex", {"t2id": 0, "t2name": "ted" , "t2phone": "6548-9874"})
    db.insertInto("table2_ex", {"t2id": 1, "t2name": "fred", "t2phone": "6548-1513"})
    db.insertInto("table2_ex", {"t2id": 2, "t2name": "ned" , "t2phone": "1111-9899"})

def print_rows (data) :
    for row in data :
        keys = row.keys()
        keys.sort()
        row = map(row.get, keys)
        for val in row :
           print val, "\t",
        print

if __name__ == '__main__' :
    
    if 'example' not in os.listdir(".") :
        createEx()
    
    dbms = DBMS('example', '.')
    db = dbms.useDatabase("db_example")

    if not db.tables["table1_ex"].data or not db.tables["table2_ex"].data :
        populate(db)

    print "table1_ex"
    print_rows(db.tables["table1_ex"].data)
    print "table2_ex"
    print_rows(db.tables["table2_ex"].data)

    db.deleteFrom("table1_ex", "t1name == 'jair'")
    db.deleteFrom("table2_ex", "t2id == 2")

    db.update("table1_ex", "t1phone == '6548-9874'", {'t1phone':'0'})
    db.update("table2_ex", "t2name == 'ted'", {'t2phone':'8'})

    print "--"
    print "table1_ex"
    print_rows(db.tables["table1_ex"].data)
    print "table2_ex"
    print_rows(db.tables["table2_ex"].data)

