#encoding:utf-8

from items import models
import os, requests, json, re

# Google Books

def book_create(originId):
	api_key = os.environ['GOOGLE_API_KEY']
	url = "https://www.googleapis.com/books/v1/volumes/" + originId + "?key=" + api_key
	fields = json.loads(requests.get(url).text)['volumeInfo']
	book = models.Book()
	book.title = fields['title']
	book.year = fields['publishedDate'][0:4]
	if 'description' in fields:
		book.description = re.sub("<.*?>", "", fields['description'])
	if 'imageLinks' in fields:
		images = fields['imageLinks']
		if 'medium' in images:
			book.image = images['medium'].partition("&imgtk")[0]
		elif 'small' in images:
			book.image = images['small'].partition("&imgtk")[0]
		elif 'large' in images:
			book.image = images['large'].partition("&imgtk")[0]
		elif 'extraLarge' in images:
			book.image = images['extraLarge'].partition("&imgtk")[0]
		elif 'thumbnail' in images:
			book.image = images['thumbnail'].partition("&imgtk")[0]
		elif 'smallThumbnail' in images:
			book.image = images['smallThumbnail'].partition("&imgtk")[0]
	book.originId = originId
	book.save()
	return book

# The Movie Database

def movie_create(originId):
	api_key = os.environ['TMDB_API_KEY']
	url = "https://api.themoviedb.org/3/movie/" + originId + "?api_key=" + api_key + "&language=es-ES"
	fields = json.loads(requests.get(url).text)
	movie = models.Movie()
	movie.title = fields['title']
	movie.year = fields['release_date'][0:4]
	if fields['overview']:
		movie.description = fields['overview']
	if fields['poster_path']:
		movie.image = "http://image.tmdb.org/t/p/w342" + fields['poster_path']
	if fields['runtime']:
		movie.duration = fields['runtime']
	else:
		movie.duration = 0
	movie.originId = originId
	movie.save()
	for g in fields['genres']:
		try:
			genre = models.Genre.objects.get(name=g['name'])
			movie.genres.add(genre)
		except models.Genre.DoesNotExist:
			if g['name']=="Documental":
				movie.category = "doc"
				movie.save()
	return movie

def series_create(originId):
	api_key = os.environ['TMDB_API_KEY']
	url = "https://api.themoviedb.org/3/tv/" + originId + "?api_key=" + api_key + "&language=es-ES"
	fields = json.loads(requests.get(url).text)
	series = models.Series()
	series.title = fields['name']
	series.year = fields['first_air_date'][0:4]
	if fields['overview']:
		series.description = fields['overview']
	if fields['poster_path']:
		series.image = "http://image.tmdb.org/t/p/w342" + fields['poster_path']
	if fields['status']:
		status = fields['status']
		if status == "Canceled":
			series.status = "can"
		elif status == "Ended":
			series.status = "fin"
		elif status == "Returning Series":
			series.status = "esp"
	series.originId = originId
	series.save()
	for g in fields['genres']:
		try:
			genre = models.Genre.objects.get(name=g['name'])
			series.genres.add(genre)
		except models.Genre.DoesNotExist:
			if g['name']=="Documental":
				series.category = "doc"
				series.save()
	# Chapters creation
	for s in fields['seasons']:
		season = s['season_number']
		season_url = "https://api.themoviedb.org/3/tv/" + originId + "/season/" + str(season) \
				+ "?api_key=" + api_key + "&language=es-ES"
		season_fields = json.loads(requests.get(season_url).text)
		chapters = season_fields['episodes']
		for c in chapters:
			chapter = models.Chapter()
			chapter.series = series
			chapter.season = season
			chapter.number = c['episode_number']
			chapter.name = c['name']
			chapter.save()
	return series

# Comic Vine

def comic_series_create(originId):
	api_key = os.environ['CVINE_API_KEY']
	url = "https://www.comicvine.gamespot.com/api/volume/" + originId + "/?api_key=" + api_key + "&format=JSON"
	fields = json.loads(requests.get(url, headers={'user-agent': 'enthub'}).text)['results']
	comic = models.ComicSeries()
	comic.title = fields['name']
	comic.year = fields['start_year']
	if fields['deck']:
		comic.description = fields['deck']
	if fields['image']:
		comic.image = fields['image']['small_url']
	comic.originId = originId
	comic.save()
	# Numbers creation
	if 'issues' in fields:
		for issue in fields['issues']:
			try:
				number = models.Number()
				number.number = issue['issue_number']
				if issue['name']:
					number.name = issue['name'][:100]
				else:
					number.name = "Número " + str(issue['issue_number'])
				number.comic = comic
				number.save()
			except:
				pass
	return comic

# Giant Bomb

def game_create(originId):
	api_key = os.environ['GBOMB_API_KEY']
	url = "https://www.giantbomb.com/api/game/" + originId + "/?api_key=" + api_key + "&format=JSON"
	fields = json.loads(requests.get(url, headers={'user-agent': 'enthub'}).text)['results']
	game = models.Game()
	game.title = fields['name']
	if fields['original_release_date']:
		game.year = fields['original_release_date'][0:4]
	else:
		game.year = fields['expected_release_year']
	if fields['deck']:
		game.description = fields['deck']
	if fields['image']:
		game.image = fields['image']['small_url']
	game.originId = originId
	game.save()
	# Platforms
	if fields['platforms']:
		for p in fields['platforms']:
			try:
				platform = models.Platform.objects.get(name=p['name'])
				game.platforms.add(platform)
			except models.Platform.DoesNotExist:
				url = p['api_detail_url'].replace("\\", "") + "?api_key=" + api_key + "&format=JSON"
				pfields = json.loads(requests.get(url, headers={'user-agent': 'enthub'}).text)['results']
				platform = models.Platform()
				platform.name = pfields['name']
				platform.short = pfields['abbreviation']
				if pfields['image']:
					platform.image = pfields['image']['small_url']
				platform.save()
				game.platforms.add(platform)
	# DLCs creation
	if 'dlcs' in fields:
		for d in fields['dlcs']:
			try:
				url = d['api_detail_url'].replace("\\", "") + "?api_key=" + api_key + "&format=JSON"
				dfields = json.loads(requests.get(url, headers={'user-agent': 'enthub'}).text)['results']
				dlc = models.DLC()
				dlc.game = game
				dlc.title = dfields['name']
				dlc.year = dfields['release_date'][0:4]
				if dfields['deck']:
					dlc.description = dfields['deck']
				if dfields['image']:
					dlc.image = dfields['image']['small_url']
				dlc.save()
				# Platform
				if dfields['platform']:
					p = dfields['platform']
					try:
						platform = models.Platform.objects.get(name=p['name'])
						dlc.platforms.add(platform)
					except models.Platform.DoesNotExist:
						url = p['api_detail_url'].replace("\\", "") + "?api_key=" + api_key + "&format=JSON"
						pfields = json.loads(requests.get(url, headers={'user-agent': 'enthub'}).text)['results']
						platform = models.Platform()
						platform.name = pfields['name']
						platform.short = pfields['abbreviation']
						if pfields['image']:
							platform.image = pfields['image']['small_url']
						platform.save()
						dlc.platforms.add(platform)
			except:
				pass
	return game