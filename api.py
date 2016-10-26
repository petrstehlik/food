# -*- coding: utf-8 -*-

from flask import Flask
import json
import pycurl
from io import StringIO
from io import BytesIO
from bs4 import BeautifulSoup

from cesta import kralovska_cesta
from molino import molino
from menza import menza

app = Flask(__name__)

rest_d = {

	16506890 : {"name" : "Camel"},
	16505998 : {"name" : "U 3 opic"},
	16506806 : {"name" : "Pad Thai"},
	18235286 : {"name" : "Kralovská cesta", "url" : "http://www.kralovskacesta.com"},
	16506807 : {"name" : "Velorex"},
	16505905 : {"name" : "Bavorska"},
	16511895 : {"name" : "Molino", "url" : ""},
	10000000 : {"name" : "Menza starý pivovar", "url" : "http://www.kam.vutbr.cz/?p=menu&provoz=5"}
}

def url(id):
	return('https://developers.zomato.com/api/v2.1/dailymenu?res_id=' + str(id))

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
	buf_str = buf.getvalue()
	buf_un = json.loads(str(buf_str, 'utf8'))
	return(json.dumps(buf_un, ensure_ascii=False).encode('utf8'))

@app.route('/restaurants', methods=['GET'])
def all_rest():
	return("not implemented", 501)

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_rest_by_id(id):
	result = None

	try:
		if "url" not in rest_d[id]:
			result = zomato_rest(id)
		else:
			print("should fetch the webpage " + rest_d[id]["url"] + " and parse it")
			if id == 10000000:
				result = menza()
			elif id == 18235286:
				result = kralovska_cesta()
			elif id == 16511895:
				 result = molino()

		result["name"] = rest_d[id]["name"]
	except Exception as e:
		print("Error: " + str(e))
		return(json.dumps({"error" : "Restaurant with given ID doesn't exist"}), 404)

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
