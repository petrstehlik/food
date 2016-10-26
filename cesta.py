import requests
from bs4 import BeautifulSoup

def kralovska_cesta():

	page = requests.get('http://www.kralovskacesta.com')

	soup = BeautifulSoup(page.content, "lxml")

	menu = soup.find_all("div", class_="denni-menu")

	data = menu[0].find("p", "termin")

	res = {"menu" : {"start_date" : data.string,
			"end_date" : data.string,
			"dishes" : []
			}}

	dishes = menu[0].find_all("li")

	for dish in dishes:
		res['menu']["dishes"].append({"dish" : {
			"name" : dish.get_text().replace('\n', '').replace('\r', ''),
			}})

	return res

if __name__ == "__main__":
	print(kralovska_cesta())
