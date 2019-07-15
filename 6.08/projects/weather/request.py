import requests
import datetime
import sqlite3
import sys
sys.path.append("__HOME__/weather")

def request_handler(request):
	
	if('lat' in request["args"] and 'lon' in request["args"] and 'option' in request["args"]):

	    lat = request["values"]['lat']
	    lon = request["values"]['lon']
	    option = request['values']['option']
	    try:
	    	
	    	return weatherRequest(float(lon),float(lat),option)
	         
	    except ValueError:
	        return  "Both lat and lon must be valid numbers."
	else:
	    return "You must enter an lat and lon value."

def weatherRequest(lon, lat,option):
	
	link = """https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&APPID=33c4737767bc75983ec54403a7ac55c9"""%(str(lon),str(lat))
	
	r = requests.get(link)
	
	r = r.json()
	
	time = datetime.datetime.now()
	ret = ""
	if(option == "1"):
		#The temp is 37.3 deg F
		
		temp = (float(r["main"]["temp"])-273.15) * 9/5 + 32

		ret =  "The temp is {:04.2f} deg F".format(temp)

	elif(option == "2"):
		
		am = ""
		hr = 0;
		if(time.hour>12):
			am = "PM"
			hr = time.hour-12

		else:
			am = "AM"
			hr = time.hour
		if(time.hour == 0):
			am = "AM"
			hr = 12
		#The time is 7:30 PM
		minute = ""
		if(time.minute<10):
			minute = "0"+str(time.minute)
		else:
			minute = str(time.minute)
		ret =  "The time is "+ str(hr)+":"+minute+ " "+am	
	elif(option == "3"):
		ret =  "The time is "+ str(time.month)+"/"+str(time.day)+"/"+str(time.year)
	else:
		v = r["weather"][0]["main"]
		ret =  "The visibility is " + v 
		

	

	example_db = "__HOME__/weather/time_example.db" # just come up with name of database
	conn = sqlite3.connect(example_db)  # connect to that database (will create if it doesn't already exist)
	c = conn.cursor()  # make cursor into database (allows us to execute commands)
	c.execute('''CREATE TABLE IF NOT EXISTS dated_table (val text, timing timestamp);''') # run a CREATE TABLE command
	c.execute('''INSERT into dated_table VALUES (?,?);''',(ret,datetime.datetime.now()))	
	things =  c.execute('''SELECT * FROM dated_table ORDER BY timing DESC LIMIT 5;''').fetchall()

	ans = ""
	for i in things:
		ans+=i[0]+"\n"
	conn.commit() # commit commands
	conn.close() # close connection to database
	return ans

	
