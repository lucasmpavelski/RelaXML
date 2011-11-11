from DBMS import DBMS

if __name__ == '__main__':
    dbms = DBMS('example', '.')

    #dbms.createDatabase("db_example")
    db = dbms.useDatabase("db_example")

    #columns = {"name" : "str", "favorite number" : "complex"}
    #db.createTable("tb_ex", columns)

    db.insertInto("tb_ex", {"name":"asdf", "favorite number":420j})



    print db.fromTables(["tb_ex"]).where("name == 'Lucas'").select(["favorite number"])[0]["favorite number"]
    print db.fromTables(["tb_ex"]).where("name == 'Lucas'").select(["name"])[0]["name"]
