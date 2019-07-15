import sqlite3
example_db = "example.db" # just come up with name of database
 
def create_database():
    conn = sqlite3.connect(example_db)  # connect to that database (will create if it doesn't already exist)
    c = conn.cursor()  # make cursor into database (allows us to execute commands)
    c.execute('''CREATE TABLE test_table (user text,favorite_number int);''') # run a CREATE TABLE command
    conn.commit() # commit commands
    conn.close() # close connection to database
 
# create_database()  #call the function!

def insert_into_database():
    conn = sqlite3.connect(example_db)
    c = conn.cursor()
    c.execute('''INSERT into test_table VALUES ('moises',5);''')
    conn.commit()
    conn.close()
 
# insert_into_database() #call this function!
import random
import string
 
def lotsa_inserts():
    conn = sqlite3.connect(example_db)
    c = conn.cursor()
    for x in range(100000):
        number = random.randint(0,1000000) # generate random number from 0 to 1000000
        user = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10)) # make random user name
        c.execute('''INSERT into test_table VALUES (?,?);''',(user,number))
    conn.commit()
    conn.close()
 
lotsa_inserts() #Call this function!

def lookup_database():
    conn = sqlite3.connect(example_db)
    c = conn.cursor()
    things = c.execute('''SELECT * FROM test_table WHERE favorite_number BETWEEN 1132 AND 1185 ORDER BY favorite_number DESC;''').fetchall()
    for row in things:
        print(row)
    conn.commit()
    conn.close()
 
lookup_database()#call it!