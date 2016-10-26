import requests
from datetime import datetime
from bs4 import BeautifulSoup

def menza():

	page = requests.get('http://www.kam.vutbr.cz/?p=menu&provoz=5')

	soup = BeautifulSoup(page.content, "lxml")

	menu = soup.find_all("table", class_="htab")
	#print(menu[0].encode('utf-8').strip())
	res = {"menu" : {"start_date" : "",
			"end_date" : "",
			"dishes" : []
			}}

	for row in menu[0].find_all("tr"):
		name = row.find("td", class_="levyjid")
		print(name.get_text().encode('utf-8'))
		res['menu']["dishes"].append({"dish" : {
			"name" : name.get_text()
			}})

	return res

if __name__ == "__main__":
	print(menza())
