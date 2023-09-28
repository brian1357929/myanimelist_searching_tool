
import requests
import json
import csv
import sys

count = 0


start=1
end=52000

w = open('Anime.csv', 'w',encoding='UTF-8',newline='')
w1 = open('studios.csv', 'w',encoding='UTF-8',newline='')
w2 = open('genres.csv', 'w',encoding='UTF-8',newline='')


w.write('animeID,name,season,year,type,episodes,source,scored,scoredBy,members,url\n')
w1.write('animeID,studios\n')
w2.write('animeID,genres\n')

writer = csv.writer(w)
writer1 = csv.writer(w1)
writer2 = csv.writer(w2)

for i in range(start, end):
	apiUrl = 'http://api.jikan.moe/v4/anime/' + str(i)

	# API call
	page = requests.get(apiUrl)
	c = page.content

	# Decoding JSON
	try:
		print('Fetching JSON...')
	except:
		print("Unexpected error:", sys.exc_info()[0])
		continue

	Data  = json.loads(c)


	if(page.status_code == 200):
		count = count + 1

		print('\nWriting to file...')

		l = []


		jsonData=Data['data']
		print('Reading', jsonData['title'], 'animelist...')


		for j in range(0, len(jsonData['studios'])):
			l1=[]
			l1.append(i)
			l1.append(jsonData['studios'][j]['name'])
			l1=[l1]
			writer1.writerows(l1)

		# getting genre
		for k in range(0, len(jsonData['genres'])):
			l2=[]
			l2.append(i)
			l2.append(jsonData['genres'][k]['name'])
			l2=[l2]
			writer2.writerows(l2)

		l.append(i)
		l.append(jsonData['title'])
		l.append(jsonData['season'])
		l.append(jsonData['year'])
		l.append(jsonData['type'])
		l.append(jsonData['episodes'])
		l.append(jsonData['source'])
		l.append(jsonData['score'])
		l.append(jsonData['scored_by'])
		l.append(jsonData['members'])
		l.append(jsonData['url'])
		l = [l]

		print('Writing anime', jsonData['title'])
		print('Total Anime stored in  the session:', count)
		print('Index of anime to be written:', i)

		writer.writerows(l)

w.close()
w1.close()
w2.close()

print('No more anime left. Done.\nOutput file:', outputFile)
