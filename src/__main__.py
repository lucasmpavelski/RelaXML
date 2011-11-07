from DBMS import DBMS

if __name__ == '__main__':
    #dbms = DBMS('example', '.')

    #dbms.createDatabase("db_example")
    #db = dbms.useDatabase("db_example")

    #columns = {"name" : "str", "favorite number" : "complex"}
    #db.createTable("tb_ex", columns)

    #db.insertInto("tb_ex", {"name":"Lucas", "favorite number":42j})

    #print db.tables["tb_ex"][0]["name"]

    from Result import Result

    r = Result()
    data = [{"col1":13, "col2":4 },
              {"col1":84, "col2":54},
              {"col1":45, "col2":11},
              {"col1":45, "col2":45},
              {"col1":87, "col2":77},
              {"col1":44, "col2":0 },
              {"col1":87, "col2":0 },
              {"col1":84, "col2":5 }]

    r.data = data
    r.columns = ["col1", "col2"]
    print r.orderBy("col2").data
    print r.orderBy("col1").data
    print r.where("col1 == 45").data
