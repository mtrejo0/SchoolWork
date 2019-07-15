import sqlite3
import datetime
import sys
visits_db = '__HOME__/data.db'
sys.path.append('__HOME__/treasure')
def request_handler(request):
    conn = sqlite3.connect(visits_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS locations (location text);''') # run a CREATE TABLE command
    if (request['method']=='POST'):
        conn = sqlite3.connect(visits_db) 
        c = conn.cursor()  
        locs = ["Student Center", "Dorm Row", "Simmons/Briggs", "Infinite Corridor/Killian", "East Campus"]
        c.execute('''DELETE FROM locations;''')

        for i in range(len(locs)):
            c.execute('''INSERT into locations VALUES (?);''', (locs[i],))

       
        conn.commit() 
        conn.close() 

    elif (request['method']=='GET'):
        conn = sqlite3.connect(visits_db)  # connect to that database (will create if it doesn't already exist)
        c = conn.cursor()  # make cursor into database (allows us to execute commands)

        try:
            lon = float(request['values']['lat'])
            lat = float(request['values']['lon'])
        except:
            return "You must enter a valid lat and lon value"
        position = get_area((lat, lon))
        location = c.execute('''SELECT * FROM locations LIMIT 1;''').fetchone()
        
        if location is None:
            return "You Won!"

        if (position == location[0]):
            c.execute('''DELETE FROM locations LIMIT 1;''')
            location = c.execute('''SELECT * FROM locations LIMIT 1;''').fetchone()

       
        conn.commit()
        conn.close() 

        return "Go to "+location[0]
def bounding_box(p,box):
    box.sort()
    if(p[0]>box[0][0] and p[0]< box[3][0] and p[1]>box[0][1] and p[1]< box[3][1]):
    	return True
    else:
    	return False
    pass # Your code here
def within_area(point,poly):
	for i in range(len(poly)):
		p = poly[i]
		poly[i] = (p[0]-point[0],p[1]-point[1])
	
	edges = []
	for i in range(len(poly)-1):
		p1 = poly[i]
		p2 = poly[i+1]
		if(p1[1]*p2[1]<0):
			edges +=[[p1,p2]]

	p1 = poly[0]
	p2 = poly[-1]
	if(p1[1]*p2[1]<0):
		edges +=[[p1,p2]]

	count = 0
	
	for i in edges:
		if(i[0][0] > 0  and i[1][0] > 0):
			count+=1
		elif(not (i[0][0] == i[1][0]) and not (i[0][1] == i[1][1])):
			p = (i[0][0] *i[1][1] - i[0][1]*i[1][0])/(i[1][1]-i[0][1])
			if(p>0):
				count+=1
	if(count %2 == 1):
		return True
	else:
		return False
def get_area(point_coord):
	locations={
    "Student Center":[(-71.095863,42.357307),(-71.097730,42.359075),(-71.095102,42.360295),(-71.093900,42.359340),(-71.093289,42.358306)],
    "Dorm Row":[(-71.093117,42.358147),(-71.092559,42.357069),(-71.102987,42.353866),(-71.106292,42.353517)],
    "Simmons/Briggs":[(-71.097859,42.359035),(-71.095928,42.357243),(-71.106356,42.353580),(-71.108159,42.354468)],
    "Boston FSILG (West)":[(-71.124664,42.353342),(-71.125737,42.344906),(-71.092478,42.348014),(-71.092607,42.350266)],
    "Boston FSILG (East)":[(-71.092409,42.351392),(-71.090842,42.343589),(-71.080478,42.350900),(-71.081766,42.353771)],
    "Stata/North Court":[(-71.091636,42.361802),(-71.090950,42.360811),(-71.088353,42.361112),(-71.088267,42.362476),(-71.089769,42.362618)],
    "East Campus":[(-71.089426,42.358306),(-71.090885,42.360716),(-71.088310,42.361017),(-71.087130,42.359162)],
    "Vassar Academic Buildings":[(-71.094973,42.360359),(-71.091776,42.361770),(-71.090928,42.360636),(-71.094040,42.359574)],
    "Infinite Corridor/Killian":[(-71.093932,42.359542),(-71.092259,42.357180),(-71.089619,42.358274),(-71.090928,42.360541)],
    "Kendall Square":[(-71.088117,42.364188),(-71.088225,42.361112),(-71.082774,42.362032)],
    "Sloan/Media Lab":[(-71.088203,42.361017),(-71.087044,42.359178),(-71.080071,42.361619),(-71.082796,42.361905)],
    "North Campus":[(-71.11022,42.355325),(-71.101280,42.363934),(-71.089950,42.362666),(-71.108361,42.354484)],
    "Technology Square":[(-71.093610,42.363157),(-71.092130,42.365837),(-71.088182,42.364188),(-71.088267,42.362650)]
	}
	for i in locations:
		if(within_area(point_coord,locations[i])):
			return i
	return "Outside MIT"