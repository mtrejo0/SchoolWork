import requests
import datetime
import sqlite3
import sys
from bs4 import BeautifulSoup


sys.path.append("__HOME__/wiki")

def request_handler(request):
	if('topic' in request["args"] and "len" in request["args"]):
		top = request["values"]['topic']
		length = request["values"]['len']
		try:
			return wikiReq(top,int(length))
		except ValueError:
			return  '-1'	
		else:
			return '-1'
	return '-1'
def wikiReq(request,length):
	#your code here!
	topic = request
	#use the string below for properly formatted wikipedia api access (https://www.mediawiki.org/wiki/API:Main_page)
	to_send = "https://en.wikipedia.org/w/api.php?titles={}&action=query&prop=extracts&redirects=1&format=json&exintro=".format(topic)
	r = requests.get(to_send)
	data = r.json()
	#starter line for debugging:
	text = ""
	try:
		if("query" in data):
			if("pages" in data["query"]):
				for i in data["query"]["pages"]:
					text = data["query"]["pages"][i]["extract"]
			else:
				return '-1'
		else:
			return '-1'
	except KeyError:
		return "-1"
	soup = BeautifulSoup(text, 'html.parser')
	ans = soup.get_text()[:length]
	ans = ans.replace('\n',' ')
	i = len(ans)-1
	while(i>=0):
		if(ans[i] == "."):
			break
		i-=1
	ans = ans[:i+1]
	i = 0
	while(i<len(ans)):
		if(ans[i] != " "):
			break
		i+=1

	return ans[i:]
