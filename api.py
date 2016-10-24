# -*- coding: utf-8 -*-

from flask import Flask
import json
import pycurl
from io import StringIO
from io import BytesIO
from bs4 import BeautifulSoup

app = Flask(__name__)

"""
Velorex		16506807
Kralovska cesta	18235286 -- nema denni menu
Pad Thai	16506806
U 3 Opic	16505998
Camel		16506890
"""

restaurants = {
	"camel" : 16506890, 
	"opice" : 16505998,
	"pad_thai" : 16506806,
	"kralovska_cesta" : 18235286,
	"velorex" : 16506807,
	"bavorska" : 16505905
}

rest_l = [{"name" : "Camel", "id" : 16506890},
	{"name" : "U 3 Opic", "id" : 16505998},
	{"name" : "Pad Thai", "id" : 16506806},
	{"name" : "Kralovská cesta", "url" : "http://www.kralovskacesta.com"},
	{"name" : "Velorex", "id" : 16506807},
	{"name" : "Bavorska", "id" : 16505905},
	{"name" : "Menza", "url" : "http://www.kam.vutbr.cz/?p=menu&provoz=5"}
]

rest_d = {

	16506890 : {"name" : "Camel"},
	16505998 : {"name" : "U 3 opic"},
	16506806 : {"name" : "Pad Thai"},
	18235286 : {"name" : "Kralovská cesta", "url" : "http://www.kralovskacesta.com"},
	16506807 : {"name" : "Velorex"},
	16505905 : {"name" : "Bavorska"},
	10000000 : {"name" : "Menza starý pivovar", "url" : "http://www.kam.vutbr.cz/?p=menu&provoz=5"}
}

def url(id):
	return('https://developers.zomato.com/api/v2.1/dailymenu?res_id=' + str(id))


def fetch_page(url_addr):
	buf = BytesIO()
	api = pycurl.Curl()
	api.setopt(api.URL, url_addr)
	api.setopt(api.WRITEDATA, buf)
	api.perform()
	api.close()
	buf_str = buf.getvalue()

	page = buf_str#BeautifulSoup(buf_str, 'html.parser')
	return(page)

def get_menza(page):
	pass

	#for table in page.findall("table"):
	#	print(table)

	#table = page.find("table", {"id" : "m5"})
	#table_rows = table.findAll("tr")

	#for row in table.find_all('tr')[1:]:
		#print(row)
	#return({ "menu" : page.prettify()})

def get_kral(page):
	pass

@app.route("/", methods=['GET'])
def index():
	buf = BytesIO()
	api = pycurl.Curl()
	api.setopt(api.URL, url(16506890))
	api.setopt(api.WRITEDATA, buf)
	api.setopt(api.HTTPHEADER, ['user_key: a5f5fc339646b270219542f96a157bdf',
		'Accept: application/json; charset=utf8', 
		'content-type: application/json; charset=utf8'])
	api.perform()
	api.close()
	#data = buf.getvalue().decode('utf-8')
	buf_str = buf.getvalue()
	buf_un = json.loads(str(buf_str, 'utf8'))
	return(json.dumps(buf_un, ensure_ascii=False).encode('utf8'))
	#data = buf_str.encode('utf_8')
	#print(data)
	#menu = json.loads(buf.getvalue(), encoding="utf8")

	#print(json.dumps(menu))
	#return(json.dumps(menu))

@app.route('/restaurants', methods=['GET'])
def all_rest():
	result = {}
	for item in restaurants:
		print(item)
		result[item] = rest(restaurants[item])
	return(json.dumps(result,ensure_ascii=False).encode('utf8'))
		  

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_rest_by_id(id):
	result = None
	try:
		if "url" not in rest_d[id]:
			result = zomato_rest(id)
		else:
			print("should fetch the webpage " + rest_d[id]["url"] + " and parse it")
			page = fetch_page(rest_d[id]["url"])
			if id == 10000000:
				result = get_menza(page)
			elif id == 18235286:
				result = get_kral(page)
		
		result["name"] = rest_d[id]["name"]
	except Exception as e:
		print("Error: " + str(e))
		return(json.dumps({"error" : "Restaurant with given ID doesn't exist"}))

	return(json.dumps(result, ensure_ascii=False).encode('utf8'))

def zomato_rest(id):
	buf = BytesIO()
	api = pycurl.Curl()
	api.setopt(api.URL, url(id))
	api.setopt(api.WRITEDATA, buf)
	api.setopt(api.HTTPHEADER, ['user_key: a5f5fc339646b270219542f96a157bdf',
		'Accept: application/json; charset=utf8', 
		'content-type: application/json; charset=utf8'])
	api.perform()
	api.close()
	buf_str = buf.getvalue()
	buf_un = json.loads(str(buf_str, 'utf8'))
	
	if buf_un["status"] != "success" and buf_un["code"] != 200:
		return({"error" : "Encountered error code " + str(buf_un["code"])})
	
	return({"menu" : buf_un["daily_menus"][0]["daily_menu"]})

if __name__ == "__main__":
    app.run(debug=True)
