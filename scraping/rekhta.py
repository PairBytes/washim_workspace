from bs4 import BeautifulSoup
import requests
from csv import writer
import re

url= "https://www.rekhta.org/poets/bashir-badr/ghazals"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
# print('Soup:',soup)
lists = soup.find_all('div', class_='rt_bodyTitle')
# print('lists:',lists)


i=0
for l1 in lists:
    i=i+1
    title = l1.find('h3',  class_="noPoetSubTtl").text
    print()
    print(i,'.',title)
    print('_________________________________________________________________________')

    # try:
    #     year = l1.find('span',class_='poetListDate').text
    # except:
    #     year:''
    # print('Year:',year)

# for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
#     print(link.get('href'))  

