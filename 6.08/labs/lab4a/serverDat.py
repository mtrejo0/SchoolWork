import sqlite3
import datetime
visits_db = '__HOME__/dat/time_example2.db'
 
def request_handler(request):
    conn = sqlite3.connect(visits_db)  # connect to that database (will create if it doesn't already exist)
    c = conn.cursor()  # make cursor into database (allows us to execute commands)
    outs = ""
    c.execute('''CREATE TABLE IF NOT EXISTS dated_table (user text,favorite_number int, timing timestamp);''') # run a CREATE TABLE command
    fifteen_minutes_ago = datetime.datetime.now()- datetime.timedelta(minutes = 15) # create time for fifteen minutes ago!
    c.execute('''INSERT into dated_table VALUES (?,?,?);''', ('joe','5',datetime.datetime.now()))
    things = c.execute('''SELECT * FROM dated_table WHERE timing > ? ORDER BY timing ASC;''',(fifteen_minutes_ago,)).fetchall()
    outs = "Things:\n"
    for x in things:
        outs+=str(x)+"\n"
    conn.commit() # commit commands
    conn.close() # close connection to database
    return outs