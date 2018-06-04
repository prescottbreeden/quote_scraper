# http://quotes.toscrape.com
import requests
from bs4 import BeautifulSoup
from time import sleep
from csv import writer
from random import choice

all_quotes = []
base_url = 'http://quotes.toscrape.com'
url = '/page/1'

# scrape each page
while url:
	res = requests.get(f'{base_url}{url}')
	print(f'Now Scraping {base_url}{url}...')
	soup = BeautifulSoup(res.text, 'html.parser')
	quotes = soup.find_all(class_="quote")

	# extract text, author, bio link
	for quote in quotes:
		text = quote.find(class_='text').get_text()
		# word = 'the'
		# text = text.replace(word,'###')
		# text = text.replace('and','&&&')
		# text = text.replace('is','$$')
		author = quote.find(class_='author').get_text()
		bio_link = quote.find('a')['href']

		all_quotes.append({
			'text': text,
			'author': author,
			'bio_link': bio_link,
			})

	# find next page
	next_btn = soup.find(class_='next')
	url = next_btn.find('a')['href'] if next_btn else None
	# sleep(2)

# write data to csv file
with open('quote_data.csv', 'w') as csv_file:
	csv_writer = writer(csv_file)
	csv_writer.writerow(['text','author','bio_link'])
	
	for quote in all_quotes:
		csv_writer.writerow([quote['text'], quote['author'], quote['bio_link']])



def play_game():
	quote = choice(all_quotes)
	remaining_guesses = 4
	print("Here's a quote: ")
	print(quote['text'])
	guess = ''
	while guess.lower() != quote['author'].lower() and remaining_guesses > 0:
		guess = input(f'Who said this quote? Guesses remaining: {remaining_guesses} \n')
		if guess.lower() == quote['author'].lower():
			print('YOU ARE AMAZING!!')
			play_status = input('Would you like to play again? y/n \n')
			if play_status.lower() == 'y':
				play_game()
			print('Thanks for playing!!')
			break
		remaining_guesses -= 1
		if remaining_guesses == 3:
			res = requests.get(f"{base_url}{quote['bio_link']}")
			soup = BeautifulSoup(res.text, "html.parser")
			birth_date = soup.find(class_="author-born-date").get_text()
			birth_place = soup.find(class_="author-born-location").get_text()
			print(f'HINT: Author was born on {birth_date}, {birth_place}')
		elif remaining_guesses == 2:
			print(f"HINT: Author's first name starts with {quote['author'][0]}")
		elif remaining_guesses == 1:
			last_initial = quote['author'].split(" ")[1][0]
			print(f"HINT: Author's last name starts with {last_initial}")
		else:
			print(f"The Author's name was {quote['author']}, sorry, you lose!")
			play_status = input('Would you like to play again? y/n \n')
			if play_status.lower() == 'y':
				play_game()
				return
			print('Thanks for playing!!')

play_game()








#