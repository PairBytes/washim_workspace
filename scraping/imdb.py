from bs4 import BeautifulSoup
import requests, openpyxl

excel = openpyxl.Workbook()
print(excel.sheetnames)
sheet = excel.active
sheet.title = 'Top Rated Movies'
print(excel.sheetnames)
sheet.append(['Movies Rank', 'Movie Name', 'Year of Release','IMDB Rating'])

try:

	source = requests.get('https://www.imdb.com/chart/top/')
	source.raise_for_status()
	print(source)

	soup = BeautifulSoup(source.text, 'html.parser')
	# print(soup)

	movies = soup.find('tbody', class_="lister-list").find_all('tr')
	# print(len(movies))
	for movie in movies:
		name = movie.find('td', class_="titleColumn").a.text
		# print('Name:',name)
		rank = movie.find('td', class_="titleColumn").get_text(strip=True).split('.')[0]
		# print('Rank:',rank)
		year = movie.find('td', class_="titleColumn").span.text.strip('()')
		# print("Year:",year)
		rating = movie.find('td', class_="ratingColumn imdbRating").strong.text
		# print('Rating:',rating)
		print(rank, name, year, rating)
		# break
		sheet.append([rank, name, year, rating])

except Exception as e:
	print(e)

excel.save('IMDB Movie Ratings.xlsx')