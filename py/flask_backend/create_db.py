import rethinkdb as r

conn = r.connect( "localhost", 28015)

r.db_create('heck').run(conn);

#r.db_drop('superheroes').run(conn)

r.db("heck").table_create("beacons", primary_key ='uid').run(conn)