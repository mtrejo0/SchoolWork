import sqlite3
example_db = "example.db" # just come up with name of database
 
def create_database():
    conn = sqlite3.connect(example_db)  # connect to that database (will create if it doesn't already exist)
    c = conn.cursor()  # make cursor into database (allows us to execute commands)
    c.execute('''CREATE TABLE test_table (user text,favorite_number int);''') # run a CREATE TABLE command
    conn.commit() # commit commands
    conn.close() # close connection to database
 
create_database()  #call the function!