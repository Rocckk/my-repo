import requests
from sys import argv
from os import environ, mkdir

# CONSTANTS FOR REQUESTS
KEY = 'ec1c7845'
OMDB_URL = 'http://www.omdbapi.com/?apikey='+KEY

#CONSTANT FOR USER'S HOME DIRECTORY
MOVIE_DIR = environ['HOME']+'/Movie info'

#CONSTANT FOR FILE NAME
FILE_NAME = '/movie_title.txt'

def get_movie_info(argv):
	if len(argv) == 1:
		print('Please enter the movie title which you would like to retrieve after:\
				\npython movie_finder.py')
		return
	title = argv[1:]
	if len(title) == 1:
		title_w_params = 't=' + title[0]
	else:
		title_list = [i for i in title]
		title_list = '+'.join(title_list)
		title_w_params = 't=' + title_list
	req = requests.get(OMDB_URL, params=title_w_params)
	img_url = req.json()
	if img_url['Response']!='True':
		print('Incorrect movie name or such movie does not exist')
		return
	content = req.text
	try:
		mkdir(MOVIE_DIR)
		with open(MOVIE_DIR + FILE_NAME, 'w') as file:
			file.write(content)
	except FileExistsError:
		with open(MOVIE_DIR + FILE_NAME, 'w') as file:
			file.write(content)
	if img_url['Poster'] == 'N/A':
		print('No poster was found for this movie on omdbapi.com')
		return
	img_data = requests.get(img_url['Poster']).content
	with open(MOVIE_DIR + '/poster.jpg', 'wb') as image:
		image.write(img_data)



get_movie_info(argv)
