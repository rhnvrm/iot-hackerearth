import rethinkdb as r

conn = r.connect( "localhost", 28015, db='heck')

#r.db_create('heck').run(conn);

#r.db_drop('superheroes').run(conn)

#r.db("heck").table_create("beacons").run(conn)

cursor = r.table("beacons").run(conn)
for document in cursor:
    print(document)