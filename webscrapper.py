import json
import requests
from bs4 import BeautifulSoup
import pandas
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
page_no = 1
list_restaurants = []
c = 0
for page in range(0, 6):
    print(page_no)
    response = requests.get("https://www.zomato.com/bangalore/south-bangalore-restaurants?page={0}".format(page_no),
                            headers=headers)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    search_list = soup.find_all("div", {'id': 'orig-search-list'})
    list_content = search_list[0].find_all("div", {'class': 'content'})
    for i in range(0, 15):
        c = c + 1
        res_name = list_content[i].find("a", {'data-result-type': 'ResCard_Name'})
        res_name = res_name.string.strip()
        locality = list_content[i].find("b")
        locality = locality.string.strip()
        ratings = list_content[i].find("div", {'data-variation': 'mini inverted'})
        ratings = ratings.string.split()[0]
        res_type = list_content[i].find_all("div", {'class': 'col-s-12'})
        t = []
        for x in res_type:
            t = x.find("a", {'class': 'zdark ttupper fontsize6'})
            if t is None:
                continue
            t = t.string.split()
        if ratings is None:
            continue
        votes = list_content[i].find("span", {'class': re.compile(r'rating-votes-div*')})
        if votes is None:
            continue
        dataframe = []
        dfObject = {
            "restaurant_id": c,
            "name": res_name,
            "area": locality,
            "restaurant_type": t,
            "rating": ratings,
            "votes": votes.string.split()[0],
        }
        list_restaurants.append(dfObject)
        if c == 80:
            break
    page_no += 1
with open('restaurants_data.json', 'w') as outfile:
    json.dump(list_restaurants, outfile, indent=4)
df = pandas.DataFrame(list_restaurants)
df.to_csv("restaurants_data.csv", index=False, header=True)
