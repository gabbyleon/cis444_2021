import psycopg2


def get_db():
    return psycopg2.connect(host="localhost", dbname="books" , user="gdln", password="eyes22")

def get_db_instance():  
    db  = get_db()
    cur  = db.cursor( )

    return db, cur 


if __name__ == "__main__":
    db, cur = get_db_instance()

    #cur.execute("select * from users")
    #for r in cur.fetchall():
     #   print(r)

    #cur.execute("insert into users (username, password) values ('luis', 'hello');")
    #db.commit()
    
    cur.execute("SELECT * FROM users")
    result = cur.fetchall()
    for row in result:
        print(row)
    print("---------")   
    cur.execute("SELECT * FROM books")
    result = cur.fetchall()
    for row in result:
        print(row)
    print("---------")
    cur.execute("SELECT * FROM purchases")
    result = cur.fetchall()
    i = 0
    while i < len(result) :
        print(result[i])
        i+= 1


   # cur.execute("select * from users")
   # for r in cur.fetchall():
    # print(r)
    


