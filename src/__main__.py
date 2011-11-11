from DBMS import DBMS

if __name__ == '__main__':
    dbms = DBMS('example', '.')

    #dbms.createDatabase("db_example")
    db = dbms.useDatabase("db_example")

    #columns = {"name" : "str", "favorite number" : "complex"}
    #db.createTable("tb_ex", columns)

    print db.fromTables(["tb_ex"]).where("name == 'Lucas'").select(["favorite number"])[0]["favorite number"]
    print db.fromTables(["tb_ex"]).where("name == 'Lucas'").select(["name"])[0]["name"]

    print db.fromTables(["tb_ex"]).select().data
    db.deleteFrom("tb_ex", "name == 'testst'")
    print db.fromTables(["tb_ex"]).select().data
    
