import requests
from datetime import datetime
from bs4 import BeautifulSoup

days = ['pondeli', 'utery', 'streda', 'ctvrtek', 'patek']

def get_day():
	day = datetime.today()
	return(days[day.weekday()] + '-' + str(day.day) + '-' + str(day.month))

def molino():

	page = requests.get('http://www.molinorestaurant.cz/poledni-menu/' + get_day())

	soup = BeautifulSoup(page.content, "lxml")

	menu = soup.find_all("div", id="category-content")
	data = menu[0].find("tbody")

	res = {"menu" : {"start_date" : "",
			"end_date" : "",
			"dishes" : []
			}}


	for row in data.find_all('tr'):
		print(row)
		item = row.find_all('td')
		res['menu']["dishes"].append({"dish" : {
			"name" : item[0].get_text().replace('\n', '').replace('\r', ''),
			"price" : item[2].get_text().replace('\n', '').replace('\r', ''),
			}})

	return res

if __name__ == "__main__":
	print(molino())
