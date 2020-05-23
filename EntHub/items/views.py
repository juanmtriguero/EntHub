#encoding:utf-8

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from items import models, forms
import os, requests, json, re

# Item search

def search(request):
	items = {}
	q = request.POST.get('q', '')
	c = request.POST.get('c', 'all')
	g = request.POST.getlist('genres')
	g = [int(n) for n in g]
	aux = c=="all"
	if c == "books" or aux:
		books = models.Book.objects.filter(title__icontains=q)
		if g:
			books = books.filter(genres__pk__in=g)
		for item in books:
			try:
				option = request.user.bookmark_set.get(book=item).option
			except models.BookMark.DoesNotExist:
				option = None
			items.update({item: option})
	if c == "movies" or aux:
		movies = models.Movie.objects.filter(title__icontains=q)
		if g:
			movies = movies.filter(genres__pk__in=g)
		for item in movies:
			try:
				option = request.user.moviemark_set.get(movie=item).option
			except models.MovieMark.DoesNotExist:
				option = None
			items.update({item: option})
	if c == "series" or aux:
		series = models.Series.objects.filter(title__icontains=q)
		if g:
			series = series.filter(genres__pk__in=g)
		for item in series:
			try:
				option = request.user.seriesmark_set.get(series=item).option
			except models.SeriesMark.DoesNotExist:
				option = None
			items.update({item: option})
	if c == "comics" or aux:
		comics = models.Comic.objects.filter(title__icontains=q)
		if g:
			comics = comics.filter(genres__pk__in=g)
		for item in comics:
			try:
				option = request.user.comicmark_set.get(comic=item).option
			except models.ComicMark.DoesNotExist:
				option = None
			items.update({item: option})
		comicseries = models.ComicSeries.objects.filter(title__icontains=q)
		if g:
			comicseries = comicseries.filter(genres__pk__in=g)
		for item in comicseries:
			try:
				option = request.user.comicseriesmark_set.get(comic=item).option
			except models.ComicSeriesMark.DoesNotExist:
				option = None
			items.update({item: option})
	if c == "games" or aux:
		games = models.Game.objects.filter(title__icontains=q)
		if g:
			games = games.filter(genres__pk__in=g)
		for item in games:
			try:
				option = request.user.gamemark_set.get(game=item).option
			except models.GameMark.DoesNotExist:
				option = None
			items.update({item: option})
		dlcs = models.DLC.objects.filter(title__icontains=q)
		if g:
			dlcs = dlcs.filter(genres__pk__in=g)
		for item in dlcs:
			try:
				option = request.user.dlcmark_set.get(dlc=item).option
			except models.DLCMark.DoesNotExist:
				option = None
			items.update({item: option})
	genres = models.Genre.objects.all()
	context = {'items': items, 'q': q, 'c': c, 'genres': genres, 'g': g}
	return render(request, 'items/search.html', context)

# Book

def book_list(request):
	items = {}
	# Filter by mark
	m = request.POST.get('m')
	if m:
		if m != 'fav':
			marks = request.user.bookmark_set.filter(option=m)
		else:
			marks = request.user.bookmark_set.filter(fav='True')
		item_list = [mark.book for mark in marks]
	else:
		item_list = models.Book.objects.all()
	for item in item_list:
		try:
			option = request.user.bookmark_set.get(book=item).option
		except models.BookMark.DoesNotExist:
			option = None
		items.update({item: option})
	# Count by mark
	pen = request.user.bookmark_set.filter(option='pen').count()
	ley = request.user.bookmark_set.filter(option='ley').count()
	pau = request.user.bookmark_set.filter(option='pau').count()
	lei = request.user.bookmark_set.filter(option='lei').count()
	marks = {'pen': pen, 'ley': ley, 'pau': pau, 'lei': lei}
	fav = request.user.bookmark_set.filter(fav='True').count()
	header = 'Catálogo de libros'
	item_path = 'books'
	context = {'items': items, 'm': m, 'marks': marks, 'fav': fav,
			'header': header, 'item_path': item_path}
	return render(request, 'items/item_list.html', context)

class BookDetail(DetailView):
	model = models.Book
	template_name = 'items/item_detail.html'

	def get_context_data(self, **kwargs):
		context = super(BookDetail, self).get_context_data(**kwargs)
		context['item_path'] = 'books'
		context['item_name'] = 'Libro'
		context['agents'] = group_agents(self.object.bookinvolvement_set.all())
		context['mark_options'] = models.BookMark.OPTION_CHOICES
		try:
			mark = self.request.user.bookmark_set.get(book=self.object)
			context['mark'] = mark.option
			fav = mark.fav
			context['rate'] = mark.rating
		except models.BookMark.DoesNotExist:
			fav = False
		context['fav'] = fav
		if self.object.originId:
			context['origin_path'] = 'https://books.google.es/books?id=' + self.object.originId
			context['origin_icon'] = '/static/images/google_icon.svg'
			context['origin_name'] = 'Google Books'
		return context

class BookCreate(CreateView):
	model = models.Book
	form_class = forms.BookForm
	template_name = 'items/api_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(BookCreate, self).get_context_data(**kwargs)
		context['legend'] = "Nuevo libro"
		context['cancel_url'] = "/items/books"
		context['api_name'] = "Google Books"
		context['api_url'] = "https://books.google.com"
		context['link_placeholder'] = "https://books.google.com/books..."
		return context

	def get_success_url(self):
		return reverse_lazy('items:book_detail', 
			kwargs={'pk': self.object.id})

class BookUpdate(UpdateView):
	model = models.Book
	form_class = forms.BookForm
	template_name = 'items/item_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(BookUpdate, self).get_context_data(**kwargs)
		context['legend'] = "Editar libro"
		context['cancel_url'] = "/items/books/" + str(self.object.id)
		return context

	def get_success_url(self):
		return reverse_lazy('items:book_detail', 
			kwargs={'pk': self.object.id})

class BookDelete(DeleteView):
	model = models.Book
	context_object_name = 'item'
	template_name = 'items/item_delete.html'
	success_url = reverse_lazy('items:book_list')
	
	def get_context_data(self, **kwargs):
		context = super(BookDelete, self).get_context_data(**kwargs)
		context['message'] = "el libro"
		context['cancel_url'] = "/items/books/" + str(self.object.id)
		return context

def book_mark(request):
	user = request.user
	book_id = request.POST['id']
	try:
		mark = user.bookmark_set.get(book__id=book_id)
	except models.BookMark.DoesNotExist:
		mark = models.BookMark()
		mark.user = user
		mark.book_id = book_id
	option = request.POST.get('option')
	if option == "not":
		mark.option = ""
	else:
		mark.option = option
		# Log creation
		log = models.BookMarkLog()
		log.user = user
		log.book_id = book_id
		log.option = option
		log.save()
	mark.save()
	return HttpResponse()

def book_fav(request):
	user = request.user
	book_id = request.POST['id']
	try:
		mark = user.bookmark_set.get(book__id=book_id)
	except models.BookMark.DoesNotExist:
		mark = models.BookMark()
		mark.user = user
		mark.book_id = book_id
	fav = request.POST.get('fav')
	if fav == "unfav":
		fav = "fav"
		mark.fav = True
		# Log creation
		log = models.BookMarkLog()
		log.user = user
		log.book_id = book_id
		log.fav = True
		log.save()
	elif fav == "fav":
		fav = "unfav"
		mark.fav = False
	mark.save()
	return HttpResponse(fav)

def book_rate(request):
	user = request.user
	book_id = request.POST['id']
	old_rating = None
	try:
		mark = user.bookmark_set.get(book__id=book_id)
		old_rating = mark.rating
	except models.BookMark.DoesNotExist:
		mark = models.BookMark()
		mark.user = user
		mark.book_id = book_id
	new_rating = int(request.POST.get('rating'))
	mark.rating = new_rating
	mark.save()
	new_item_rating = update_item_rating(mark.book, old_rating, new_rating)
	# Log creation
	log = models.BookMarkLog()
	log.user = user
	log.book_id = book_id
	log.rating = new_rating
	log.save()
	return HttpResponse(new_item_rating)

def book_api(request):
	try:
		# https://books.google.es/books?id=[id]
		link = request.POST.get('link')
		gb_id = link.partition("?id=")[2].partition("&")[0]
		api_key = os.environ['GOOGLE_API_KEY']
		url = "https://www.googleapis.com/books/v1/volumes/" + gb_id + "?key=" + api_key
		fields = json.loads(requests.get(url).text)['volumeInfo']
		book = models.Book()
		book.title = fields['title']
		book.year = fields['publishedDate'][0:4]
		if 'description' in fields:
			book.description = re.sub("<.*?>", "", fields['description'])
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
		book.save()
		success_url = '/items/books/' + str(book.id)
		return JsonResponse({'success_url': success_url})
	except:
		return JsonResponse({'error': 'Por favor, introduzca un enlace válido.'})

# Movie

def movie_list(request):
	items = {}
	# Filter by mark
	m = request.POST.get('m')
	if m:
		if m != 'fav':
			marks = request.user.moviemark_set.filter(option=m)
		else:
			marks = request.user.moviemark_set.filter(fav='True')
		item_list = [mark.movie for mark in marks]
	else:
		item_list = models.Movie.objects.all()
	for item in item_list:
		try:
			option = request.user.moviemark_set.get(movie=item).option
		except models.MovieMark.DoesNotExist:
			option = None
		items.update({item: option})
	# Count by mark
	pen = request.user.moviemark_set.filter(option='pen').count()
	vis = request.user.moviemark_set.filter(option='vis').count()
	marks = {'pen': pen, 'vis': vis}
	fav = request.user.moviemark_set.filter(fav='True').count()
	header = 'Catálogo de cine y TV'
	item_path = 'movies'
	context = {'items': items, 'm': m, 'marks': marks, 'fav': fav,
			'header': header, 'item_path': item_path}
	return render(request, 'items/movie_list.html', context)

class MovieDetail(DetailView):
	model = models.Movie
	template_name = 'items/movie_detail.html'

	def get_context_data(self, **kwargs):
		context = super(MovieDetail, self).get_context_data(**kwargs)
		context['item_path'] = 'movies'
		context['item_name'] = 'Cine'
		context['agents'] = group_agents(self.object.movieinvolvement_set.all())
		context['mark_options'] = models.MovieMark.OPTION_CHOICES
		try:
			mark = self.request.user.moviemark_set.get(movie=self.object)
			context['mark'] = mark.option
			fav = mark.fav
			context['rate'] = mark.rating
		except models.MovieMark.DoesNotExist:
			fav = False
		context['fav'] = fav
		if self.object.originId:
			context['origin_path'] = 'https://www.themoviedb.org/movie/' + self.object.originId
			context['origin_icon'] = '/static/images/tmdb_icon.svg'
			context['origin_name'] = 'The Movie Database'
		return context

class MovieCreate(CreateView):
	model = models.Movie
	form_class = forms.MovieForm
	template_name = 'items/api_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(MovieCreate, self).get_context_data(**kwargs)
		context['legend'] = "Nueva película"
		context['cancel_url'] = "/items/movies"
		context['api_name'] = "The Movie Database"
		context['api_url'] = "https://www.themoviedb.org"
		context['link_placeholder'] = "https://www.themoviedb.org/movie/..."
		return context

	def get_success_url(self):
		return reverse_lazy('items:movie_detail', 
			kwargs={'pk': self.object.id})

class MovieUpdate(UpdateView):
	model = models.Movie
	form_class = forms.MovieForm
	template_name = 'items/item_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(MovieUpdate, self).get_context_data(**kwargs)
		context['legend'] = "Editar película"
		context['cancel_url'] = "/items/movies/" + str(self.object.id)
		return context

	def get_success_url(self):
		return reverse_lazy('items:movie_detail', 
			kwargs={'pk': self.object.id})

class MovieDelete(DeleteView):
	model = models.Movie
	context_object_name = 'item'
	template_name = 'items/item_delete.html'
	success_url = reverse_lazy('items:movie_list')
	
	def get_context_data(self, **kwargs):
		context = super(MovieDelete, self).get_context_data(**kwargs)
		context['message'] = "la película"
		context['cancel_url'] = "/items/movies/" + str(self.object.id)
		return context

def movie_mark(request):
	user = request.user
	movie_id = request.POST['id']
	try:
		mark = user.moviemark_set.get(movie__id=movie_id)
	except models.MovieMark.DoesNotExist:
		mark = models.MovieMark()
		mark.user = user
		mark.movie_id = movie_id
	option = request.POST.get('option')
	if option == "not":
		mark.option = ""
	else:
		mark.option = option
		# Log creation
		log = models.MovieMarkLog()
		log.user = user
		log.movie_id = movie_id
		log.option = option
		log.save()
	mark.save()
	return HttpResponse()

def movie_fav(request):
	user = request.user
	movie_id = request.POST['id']
	try:
		mark = user.moviemark_set.get(movie__id=movie_id)
	except models.MovieMark.DoesNotExist:
		mark = models.MovieMark()
		mark.user = user
		mark.movie_id = movie_id
	fav = request.POST.get('fav')
	if fav == "unfav":
		fav = "fav"
		mark.fav = True
		# Log creation
		log = models.MovieMarkLog()
		log.user = user
		log.movie_id = movie_id
		log.fav = True
		log.save()
	elif fav == "fav":
		fav = "unfav"
		mark.fav = False
	mark.save()
	return HttpResponse(fav)

def movie_rate(request):
	user = request.user
	movie_id = request.POST['id']
	old_rating = None
	try:
		mark = user.moviemark_set.get(movie__id=movie_id)
		old_rating = mark.rating
	except models.MovieMark.DoesNotExist:
		mark = models.MovieMark()
		mark.user = user
		mark.movie_id = movie_id
	new_rating = int(request.POST.get('rating'))
	mark.rating = new_rating
	mark.save()
	new_item_rating = update_item_rating(mark.movie, old_rating, new_rating)
	# Log creation
	log = models.MovieMarkLog()
	log.user = user
	log.movie_id = movie_id
	log.rating = new_rating
	log.save()
	return HttpResponse(new_item_rating)

def movie_api(request):
	try:
		# https://www.themoviedb.org/movie/[id]-[title]
		link = request.POST.get('link')
		# Link is not from TV
		assert not link.startswith("https://www.themoviedb.org/tv/")
		tmdb_id = link.partition("/movie/")[2].partition("-")[0]
		api_key = os.environ['TMDB_API_KEY']
		url = "https://api.themoviedb.org/3/movie/" + tmdb_id + "?api_key=" + api_key + "&language=es-ES"
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
		movie.save()
		for g in fields['genres']:
			try:
				genre = models.Genre.objects.get(name=g['name'])
				movie.genres.add(genre)
			except models.Genre.DoesNotExist:
				if g['name']=="Documental":
					movie.category = "doc"
					movie.save()
		success_url = '/items/movies/' + str(movie.id)
		return JsonResponse({'success_url': success_url})
	except AssertionError:
		return JsonResponse({'error': 'Por favor, introduzca el enlace de una ficha de cine.'})
	except:
		return JsonResponse({'error': 'Por favor, introduzca un enlace válido.'})

# Series

def series_list(request):
	items = {}
	# Filter by mark
	m = request.POST.get('m')
	if m:
		if m != 'fav':
			marks = request.user.seriesmark_set.filter(option=m)
		else:
			marks = request.user.seriesmark_set.filter(fav='True')
		item_list = [mark.series for mark in marks]
	else:
		item_list = models.Series.objects.all()
	for item in item_list:
		try:
			option = request.user.seriesmark_set.get(series=item).option
		except models.SeriesMark.DoesNotExist:
			option = None
		items.update({item: option})
	# Count by mark
	pen = request.user.seriesmark_set.filter(option='pen').count()
	sig = request.user.seriesmark_set.filter(option='sig').count()
	pau = request.user.seriesmark_set.filter(option='pau').count()
	fin = request.user.seriesmark_set.filter(option='fin').count()
	marks = {'pen': pen, 'sig': sig, 'pau': pau, 'fin': fin}
	fav = request.user.seriesmark_set.filter(fav='True').count()
	header = 'Catálogo de cine y TV'
	item_path = 'series'
	context = {'items': items, 'm': m, 'marks': marks, 'fav': fav,
			'header': header, 'item_path': item_path}
	return render(request, 'items/series_list.html', context)

class SeriesDetail(DetailView):
	model = models.Series
	template_name = 'items/series_detail.html'

	def get_context_data(self, **kwargs):
		context = super(SeriesDetail, self).get_context_data(**kwargs)
		context['item_path'] = 'series'
		context['item_name'] = 'Televisión'
		context['agents'] = group_agents(self.object.seriesinvolvement_set.all())
		context['label'] = self.get_label()
		context['chapters'] = self.get_chapters()
		context['mark_options'] = models.SeriesMark.OPTION_CHOICES
		try:
			mark = self.request.user.seriesmark_set.get(series=self.object)
			context['mark'] = mark.option
			fav = mark.fav
			context['rate'] = mark.rating
		except models.SeriesMark.DoesNotExist:
			fav = False
		context['fav'] = fav
		if self.object.originId:
			context['origin_path'] = 'https://www.themoviedb.org/tv/' + self.object.originId
			context['origin_icon'] = '/static/images/tmdb_icon.svg'
			context['origin_name'] = 'The Movie Database'
		return context
	
	# Set label color by status
	def get_label(self):
		if self.object.status == 'emi':
			label = 'label-primary'
		elif self.object.status == 'can':
			label = 'label-danger'
		elif self.object.status == 'fin':
			label = 'label-success'
		elif self.object.status == 'esp':
			label = 'label-info'
		else:
			label = 'label-default'
		return label

	# Return chapters by seasons
	def get_chapters(self):
		chapters = {}
		for chapter in self.object.chapter_set.all():
			if chapter.season in chapters:
				chapters[chapter.season].append(chapter)
			else:
				chapters[chapter.season] = [chapter,]
		return chapters

class SeriesCreate(CreateView):
	model = models.Series
	form_class = forms.SeriesForm
	template_name = 'items/api_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(SeriesCreate, self).get_context_data(**kwargs)
		context['legend'] = "Nueva serie"
		context['cancel_url'] = "/items/series"
		context['api_name'] = "The Movie Database"
		context['api_url'] = "https://www.themoviedb.org"
		context['link_placeholder'] = "https://www.themoviedb.org/tv/..."
		return context

	def get_success_url(self):
		return reverse_lazy('items:series_detail', 
			kwargs={'pk': self.object.id})

class SeriesUpdate(UpdateView):
	model = models.Series
	form_class = forms.SeriesForm
	template_name = 'items/item_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(SeriesUpdate, self).get_context_data(**kwargs)
		context['legend'] = "Editar serie"
		context['cancel_url'] = "/items/series/" + str(self.object.id)
		return context

	def get_success_url(self):
		return reverse_lazy('items:series_detail', 
			kwargs={'pk': self.object.id})

class SeriesDelete(DeleteView):
	model = models.Series
	context_object_name = 'item'
	template_name = 'items/item_delete.html'
	success_url = reverse_lazy('items:series_list')
	
	def get_context_data(self, **kwargs):
		context = super(SeriesDelete, self).get_context_data(**kwargs)
		context['message'] = "la serie"
		context['cancel_url'] = "/items/series/" + str(self.object.id)
		return context

def series_mark(request):
	user = request.user
	series_id = request.POST['id']
	try:
		mark = user.seriesmark_set.get(series__id=series_id)
	except models.SeriesMark.DoesNotExist:
		mark = models.SeriesMark()
		mark.user = user
		mark.series_id = series_id
	option = request.POST.get('option')
	if option == "not":
		mark.option = ""
	else:
		mark.option = option
		# Log creation
		log = models.SeriesMarkLog()
		log.user = user
		log.series_id = series_id
		log.option = option
		log.save()
	mark.save()
	return HttpResponse()

def series_fav(request):
	user = request.user
	series_id = request.POST['id']
	try:
		mark = user.seriesmark_set.get(series__id=series_id)
	except models.SeriesMark.DoesNotExist:
		mark = models.SeriesMark()
		mark.user = user
		mark.series_id = series_id
	fav = request.POST.get('fav')
	if fav == "unfav":
		fav = "fav"
		mark.fav = True
		# Log creation
		log = models.SeriesMarkLog()
		log.user = user
		log.series_id = series_id
		log.fav = True
		log.save()
	elif fav == "fav":
		fav = "unfav"
		mark.fav = False
	mark.save()
	return HttpResponse(fav)

def series_rate(request):
	user = request.user
	series_id = request.POST['id']
	old_rating = None
	try:
		mark = user.seriesmark_set.get(series__id=series_id)
		old_rating = mark.rating
	except models.SeriesMark.DoesNotExist:
		mark = models.SeriesMark()
		mark.user = user
		mark.series_id = series_id
	new_rating = int(request.POST.get('rating'))
	mark.rating = new_rating
	mark.save()
	new_item_rating = update_item_rating(mark.series, old_rating, new_rating)
	# Log creation
	log = models.SeriesMarkLog()
	log.user = user
	log.series_id = series_id
	log.rating = new_rating
	log.save()
	return HttpResponse(new_item_rating)

def series_api(request):
	try:
		# https://www.themoviedb.org/tv/[id]-[title]
		link = request.POST.get('link')
		# Link is not from movie
		assert not link.startswith("https://www.themoviedb.org/movie/")
		tmdb_id = link.partition("/tv/")[2].partition("-")[0]
		api_key = os.environ['TMDB_API_KEY']
		url = "https://api.themoviedb.org/3/tv/" + tmdb_id + "?api_key=" + api_key + "&language=es-ES"
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
			season_url = "https://api.themoviedb.org/3/tv/" + tmdb_id + "/season/" + str(season) \
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
		success_url = '/items/series/' + str(series.id)
		return JsonResponse({'success_url': success_url})
	except AssertionError:
		return JsonResponse({'error': 'Por favor, introduzca el enlace de una ficha de TV.'})
	except:
		return JsonResponse({'error': 'Por favor, introduzca un enlace válido.'})

# Chapter

class ChapterCreate(CreateView):
	model = models.Chapter
	form_class = forms.ChapterForm
	template_name = 'items/item_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(ChapterCreate, self).get_context_data(**kwargs)
		context['legend'] = "Añadir capítulo"
		context['cancel_url'] = "/items/series/" + str(self.kwargs['pk'])
		return context

	def form_valid(self, form):
		form.instance.series = models.Series.objects.get(pk=self.kwargs['pk'])
		return super(ChapterCreate, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('items:series_detail', 
			kwargs={'pk': self.kwargs['pk']})

def chapter_tic(request, chapter_id):
	user = request.user
	chapter = models.Chapter.objects.get(id=chapter_id)
	chapter.tics.add(user)
	return HttpResponse()

def chapter_untic(request, chapter_id):
	user = request.user
	chapter = models.Chapter.objects.get(id=chapter_id)
	chapter.tics.remove(user)
	return HttpResponse()

# Comic

def comic_list(request):
	items = {}
	# Filter by mark
	m = request.POST.get('m')
	if m:
		if m != 'fav':
			marks = request.user.comicmark_set.filter(option=m)
		else:
			marks = request.user.comicmark_set.filter(fav='True')
		item_list = [mark.comic for mark in marks]
	else:
		item_list = models.Comic.objects.all()
	for item in item_list:
		try:
			option = request.user.comicmark_set.get(comic=item).option
		except models.ComicMark.DoesNotExist:
			option = None
		items.update({item: option})
	# Count by mark
	pen = request.user.comicmark_set.filter(option='pen').count()
	ley = request.user.comicmark_set.filter(option='ley').count()
	pau = request.user.comicmark_set.filter(option='pau').count()
	lei = request.user.comicmark_set.filter(option='lei').count()
	marks = {'pen': pen, 'ley': ley, 'pau': pau, 'lei': lei}
	fav = request.user.comicmark_set.filter(fav='True').count()
	header = 'Catálogo de cómics'
	item_path = 'comics'
	context = {'items': items, 'm': m, 'marks': marks, 'fav': fav,
			'header': header, 'item_path': item_path}
	return render(request, 'items/comic_list.html', context)

class ComicDetail(DetailView):
	model = models.Comic
	template_name = 'items/item_detail.html'

	def get_context_data(self, **kwargs):
		context = super(ComicDetail, self).get_context_data(**kwargs)
		context['item_path'] = 'comics'
		context['item_name'] = 'Cómic'
		context['agents'] = group_agents(self.object.comicinvolvement_set.all())
		context['mark_options'] = models.ComicMark.OPTION_CHOICES
		try:
			mark = self.request.user.comicmark_set.get(comic=self.object)
			context['mark'] = mark.option
			fav = mark.fav
			context['rate'] = mark.rating
		except models.ComicMark.DoesNotExist:
			fav = False
		context['fav'] = fav
		return context

class ComicCreate(CreateView):
	model = models.Comic
	form_class = forms.ComicForm
	template_name = 'items/item_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(ComicCreate, self).get_context_data(**kwargs)
		context['legend'] = "Nuevo cómic"
		context['cancel_url'] = "/items/comics"
		return context

	def get_success_url(self):
		return reverse_lazy('items:comic_detail', 
			kwargs={'pk': self.object.id})

class ComicUpdate(UpdateView):
	model = models.Comic
	form_class = forms.ComicForm
	template_name = 'items/item_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(ComicUpdate, self).get_context_data(**kwargs)
		context['legend'] = "Editar cómic"
		context['cancel_url'] = "/items/comics/" + str(self.object.id)
		return context

	def get_success_url(self):
		return reverse_lazy('items:comic_detail', 
			kwargs={'pk': self.object.id})

class ComicDelete(DeleteView):
	model = models.Comic
	context_object_name = 'item'
	template_name = 'items/item_delete.html'
	success_url = reverse_lazy('items:comic_list')
	
	def get_context_data(self, **kwargs):
		context = super(ComicDelete, self).get_context_data(**kwargs)
		context['message'] = "el cómic"
		context['cancel_url'] = "/items/comics/" + str(self.object.id)
		return context

def comic_mark(request):
	user = request.user
	comic_id = request.POST['id']
	try:
		mark = user.comicmark_set.get(comic__id=comic_id)
	except models.ComicMark.DoesNotExist:
		mark = models.ComicMark()
		mark.user = user
		mark.comic_id = comic_id
	option = request.POST.get('option')
	if option == "not":
		mark.option = ""
	else:
		mark.option = option
		# Log creation
		log = models.ComicMarkLog()
		log.user = user
		log.comic_id = comic_id
		log.option = option
		log.save()
	mark.save()
	return HttpResponse()

def comic_fav(request):
	user = request.user
	comic_id = request.POST['id']
	try:
		mark = user.comicmark_set.get(comic__id=comic_id)
	except models.ComicMark.DoesNotExist:
		mark = models.ComicMark()
		mark.user = user
		mark.comic_id = comic_id
	fav = request.POST.get('fav')
	if fav == "unfav":
		fav = "fav"
		mark.fav = True
		# Log creation
		log = models.ComicMarkLog()
		log.user = user
		log.comic_id = comic_id
		log.fav = True
		log.save()
	elif fav == "fav":
		fav = "unfav"
		mark.fav = False
	mark.save()
	return HttpResponse(fav)

def comic_rate(request):
	user = request.user
	comic_id = request.POST['id']
	old_rating = None
	try:
		mark = user.comicmark_set.get(comic__id=comic_id)
		old_rating = mark.rating
	except models.ComicMark.DoesNotExist:
		mark = models.ComicMark()
		mark.user = user
		mark.comic_id = comic_id
	new_rating = int(request.POST.get('rating'))
	mark.rating = new_rating
	mark.save()
	new_item_rating = update_item_rating(mark.comic, old_rating, new_rating)
	# Log creation
	log = models.ComicMarkLog()
	log.user = user
	log.comic_id = comic_id
	log.rating = new_rating
	log.save()
	return HttpResponse(new_item_rating)

# ComicSeries

def comic_series_list(request):
	items = {}
	# Filter by mark
	m = request.POST.get('m')
	if m:
		if m != 'fav':
			marks = request.user.comicseriesmark_set.filter(option=m)
		else:
			marks = request.user.comicseriesmark_set.filter(fav='True')
		item_list = [mark.comic for mark in marks]
	else:
		item_list = models.ComicSeries.objects.all()
	for item in item_list:
		try:
			option = request.user.comicseriesmark_set.get(comic=item).option
		except models.ComicSeriesMark.DoesNotExist:
			option = None
		items.update({item: option})
	# Count by mark
	pen = request.user.comicseriesmark_set.filter(option='pen').count()
	sig = request.user.comicseriesmark_set.filter(option='sig').count()
	pau = request.user.comicseriesmark_set.filter(option='pau').count()
	fin = request.user.comicseriesmark_set.filter(option='fin').count()
	marks = {'pen': pen, 'sig': sig, 'pau': pau, 'fin': fin}
	fav = request.user.comicseriesmark_set.filter(fav='True').count()
	header = 'Catálogo de cómics'
	item_path = 'comicseries'
	context = {'items': items, 'm': m, 'marks': marks, 'fav': fav,
			'header': header, 'item_path': item_path}
	return render(request, 'items/comic_series_list.html', context)

class ComicSeriesDetail(DetailView):
	model = models.ComicSeries
	template_name = 'items/comic_series_detail.html'

	def get_context_data(self, **kwargs):
		context = super(ComicSeriesDetail, self).get_context_data(**kwargs)
		context['item_path'] = 'comicseries'
		context['item_name'] = 'Serie de cómics'
		context['agents'] = group_agents(self.object.comicseriesinvolvement_set.all())
		context['mark_options'] = models.ComicSeriesMark.OPTION_CHOICES
		try:
			mark = self.request.user.comicseriesmark_set.get(comic=self.object)
			context['mark'] = mark.option
			fav = mark.fav
			context['rate'] = mark.rating
		except models.ComicSeriesMark.DoesNotExist:
			fav = False
		context['fav'] = fav
		if self.object.originId:
			context['origin_path'] = 'https://comicvine.gamespot.com/comic/' + self.object.originId
			context['origin_icon'] = '/static/images/cvine_icon.svg'
			context['origin_name'] = 'Comic Vine'
		return context

class ComicSeriesCreate(CreateView):
	model = models.ComicSeries
	form_class = forms.ComicSeriesForm
	template_name = 'items/api_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(ComicSeriesCreate, self).get_context_data(**kwargs)
		context['legend'] = "Nueva serie de cómics"
		context['cancel_url'] = "/items/comicseries"
		context['api_name'] = "Comic Vine"
		context['api_url'] = "https://comicvine.gamespot.com/"
		context['link_placeholder'] = "https://comicvine.gamespot.com/..."
		return context

	def get_success_url(self):
		return reverse_lazy('items:comic_series_detail', 
			kwargs={'pk': self.object.id})

class ComicSeriesUpdate(UpdateView):
	model = models.ComicSeries
	form_class = forms.ComicSeriesForm
	template_name = 'items/item_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(ComicSeriesUpdate, self).get_context_data(**kwargs)
		context['legend'] = "Editar serie de cómics"
		context['cancel_url'] = "/items/comicseries/" + str(self.object.id)
		return context

	def get_success_url(self):
		return reverse_lazy('items:comic_series_detail', 
			kwargs={'pk': self.object.id})

class ComicSeriesDelete(DeleteView):
	model = models.ComicSeries
	context_object_name = 'item'
	template_name = 'items/item_delete.html'
	success_url = reverse_lazy('items:comic_series_list')
	
	def get_context_data(self, **kwargs):
		context = super(ComicSeriesDelete, self).get_context_data(**kwargs)
		context['message'] = "la serie de cómics"
		context['cancel_url'] = "/items/comicseries/" + str(self.object.id)
		return context

def comic_series_mark(request):
	user = request.user
	comic_id = request.POST['id']
	try:
		mark = user.comicseriesmark_set.get(comic__id=comic_id)
	except models.ComicSeriesMark.DoesNotExist:
		mark = models.ComicSeriesMark()
		mark.user = user
		mark.comic_id = comic_id
	option = request.POST.get('option')
	if option == "not":
		mark.option = ""
	else:
		mark.option = option
		# Log creation
		log = models.ComicSeriesMarkLog()
		log.user = user
		log.comicseries_id = comic_id
		log.option = option
		log.save()
	mark.save()
	return HttpResponse()

def comic_series_fav(request):
	user = request.user
	comic_id = request.POST['id']
	try:
		mark = user.comicseriesmark_set.get(comic__id=comic_id)
	except models.ComicSeriesMark.DoesNotExist:
		mark = models.ComicSeriesMark()
		mark.user = user
		mark.comic_id = comic_id
	fav = request.POST.get('fav')
	if fav == "unfav":
		fav = "fav"
		mark.fav = True
		# Log creation
		log = models.ComicSeriesMarkLog()
		log.user = user
		log.comicseries_id = comic_id
		log.fav = True
		log.save()
	elif fav == "fav":
		fav = "unfav"
		mark.fav = False
	mark.save()
	return HttpResponse(fav)

def comic_series_rate(request):
	user = request.user
	comic_id = request.POST['id']
	old_rating = None
	try:
		mark = user.comicseriesmark_set.get(comic__id=comic_id)
		old_rating = mark.rating
	except models.ComicSeriesMark.DoesNotExist:
		mark = models.ComicSeriesMark()
		mark.user = user
		mark.comic_id = comic_id
	new_rating = int(request.POST.get('rating'))
	mark.rating = new_rating
	mark.save()
	new_item_rating = update_item_rating(mark.comic, old_rating, new_rating)
	# Log creation
	log = models.ComicSeriesMarkLog()
	log.user = user
	log.comicseries_id = comic_id
	log.rating = new_rating
	log.save()
	return HttpResponse(new_item_rating)

# TODO genres
def comic_series_api(request):
	try:
		# https://www.comicvine.gamespot.com/[name]/[id]/
		link = request.POST.get('link')
		cv_id = link.partition(".com/")[2].partition("/")[2].partition("/")[0]
		api_key = os.environ['CVINE_API_KEY']
		url = "https://www.comicvine.gamespot.com/api/volume/" + cv_id + "/?api_key=" + api_key + "&format=JSON"
		fields = json.loads(requests.get(url, headers={'user-agent': 'enthub'}).text)['results']
		comic = models.ComicSeries()
		comic.title = fields['name']
		comic.year = fields['start_year']
		if fields['deck']:
			comic.description = fields['deck']
		if fields['image']:
			comic.image = fields['image']['small_url']
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
		success_url = '/items/comicseries/' + str(comic.id)
		return JsonResponse({'success_url': success_url})
	except:
		return JsonResponse({'error': 'Por favor, introduzca un enlace válido.'})

# Number

class NumberCreate(CreateView):
	model = models.Number
	form_class = forms.NumberForm
	template_name = 'items/item_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(NumberCreate, self).get_context_data(**kwargs)
		context['legend'] = "Añadir número"
		context['cancel_url'] = "/items/comicseries/" + str(self.kwargs['pk'])
		return context

	def form_valid(self, form):
		form.instance.comic = models.ComicSeries.objects.get(pk=self.kwargs['pk'])
		return super(NumberCreate, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('items:comic_series_detail', 
			kwargs={'pk': self.kwargs['pk']})

def number_tic(request, number_id):
	user = request.user
	number = models.Number.objects.get(id=number_id)
	number.tics.add(user)
	return HttpResponse()

def number_untic(request, number_id):
	user = request.user
	number = models.Number.objects.get(id=number_id)
	number.tics.remove(user)
	return HttpResponse()

# Game

def game_list(request):
	items = {}
	# Filter by mark
	m = request.POST.get('m')
	if m:
		if m != 'fav':
			marks = request.user.gamemark_set.filter(option=m)
		else:
			marks = request.user.gamemark_set.filter(fav='True')
		item_list = [mark.game for mark in marks]
	else:
		item_list = models.Game.objects.all()
	for item in item_list:
		try:
			option = request.user.gamemark_set.get(game=item).option
		except models.GameMark.DoesNotExist:
			option = None
		items.update({item: option})
	# Count by mark
	pen = request.user.gamemark_set.filter(option='pen').count()
	jug = request.user.gamemark_set.filter(option='jug').count()
	pau = request.user.gamemark_set.filter(option='pau').count()
	ter = request.user.gamemark_set.filter(option='ter').count()
	com = request.user.gamemark_set.filter(option='com').count()
	marks = {'pen': pen, 'jug': jug, 'pau': pau, 'ter': ter, 'com': com}
	fav = request.user.gamemark_set.filter(fav='True').count()
	header = 'Catálogo de videojuegos'
	item_path = 'games'
	context = {'items': items, 'm': m, 'marks': marks, 'fav': fav,
			'header': header, 'item_path': item_path}
	return render(request, 'items/item_list.html', context)

class GameDetail(DetailView):
	model = models.Game
	template_name = 'items/game_detail.html'

	def get_context_data(self, **kwargs):
		context = super(GameDetail, self).get_context_data(**kwargs)
		context['item_path'] = 'games'
		context['item_name'] = 'Videojuego'
		context['agents'] = group_agents(self.object.gameinvolvement_set.all())
		context['mark_options'] = models.GameMark.OPTION_CHOICES
		try:
			mark = self.request.user.gamemark_set.get(game=self.object)
			context['mark'] = mark.option
			fav = mark.fav
			context['rate'] = mark.rating
		except models.GameMark.DoesNotExist:
			fav = False
		context['fav'] = fav
		if self.object.originId:
			context['origin_path'] = 'https://www.giantbomb.com/game/' + self.object.originId
			context['origin_icon'] = '/static/images/gbomb_icon.svg'
			context['origin_name'] = 'Giant Bomb'
		# DLCs
		dlcs = {}
		for dlc in self.object.dlc_set.all():
			try:
				option = self.request.user.dlcmark_set.get(dlc=dlc).option
			except models.DLCMark.DoesNotExist:
				option = None
			dlcs.update({dlc: option})
		context['dlcs'] = dlcs
		return context

class GameCreate(CreateView):
	model = models.Game
	form_class = forms.GameForm
	template_name = 'items/api_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(GameCreate, self).get_context_data(**kwargs)
		context['legend'] = "Nuevo videojuego"
		context['cancel_url'] = "/items/games"
		context['api_name'] = "Giant Bomb"
		context['api_url'] = "https://www.giantbomb.com"
		context['link_placeholder'] = "https://www.giantbomb.com/..."
		return context

	def get_success_url(self):
		return reverse_lazy('items:game_detail', 
			kwargs={'pk': self.object.id})

class GameUpdate(UpdateView):
	model = models.Game
	form_class = forms.GameForm
	template_name = 'items/item_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(GameUpdate, self).get_context_data(**kwargs)
		context['legend'] = "Editar videojuego"
		context['cancel_url'] = "/items/games/" + str(self.object.id)
		return context

	def get_success_url(self):
		return reverse_lazy('items:game_detail', 
			kwargs={'pk': self.object.id})

class GameDelete(DeleteView):
	model = models.Game
	context_object_name = 'item'
	template_name = 'items/item_delete.html'
	success_url = reverse_lazy('items:game_list')
	
	def get_context_data(self, **kwargs):
		context = super(GameDelete, self).get_context_data(**kwargs)
		context['message'] = "el videojuego"
		context['cancel_url'] = "/items/games/" + str(self.object.id)
		return context

def game_mark(request):
	user = request.user
	game_id = request.POST['id']
	try:
		mark = user.gamemark_set.get(game__id=game_id)
	except models.GameMark.DoesNotExist:
		mark = models.GameMark()
		mark.user = user
		mark.game_id = game_id
	option = request.POST.get('option')
	if option == "not":
		mark.option = ""
	else:
		mark.option = option
		# Log creation
		log = models.GameMarkLog()
		log.user = user
		log.game_id = game_id
		log.option = option
		log.save()
	mark.save()
	return HttpResponse()

def game_fav(request):
	user = request.user
	game_id = request.POST['id']
	try:
		mark = user.gamemark_set.get(game__id=game_id)
	except models.GameMark.DoesNotExist:
		mark = models.GameMark()
		mark.user = user
		mark.game_id = game_id
	fav = request.POST.get('fav')
	if fav == "unfav":
		fav = "fav"
		mark.fav = True
		# Log creation
		log = models.GameMarkLog()
		log.user = user
		log.game_id = game_id
		log.fav = True
		log.save()
	elif fav == "fav":
		fav = "unfav"
		mark.fav = False
	mark.save()
	return HttpResponse(fav)

def game_rate(request):
	user = request.user
	game_id = request.POST['id']
	old_rating = None
	try:
		mark = user.gamemark_set.get(game__id=game_id)
		old_rating = mark.rating
	except models.GameMark.DoesNotExist:
		mark = models.GameMark()
		mark.user = user
		mark.game_id = game_id
	new_rating = int(request.POST.get('rating'))
	mark.rating = new_rating
	mark.save()
	new_item_rating = update_item_rating(mark.game, old_rating, new_rating)
	# Log creation
	log = models.GameMarkLog()
	log.user = user
	log.game_id = game_id
	log.rating = new_rating
	log.save()
	return HttpResponse(new_item_rating)

# TODO genres
def game_api(request):
	try:
		# https://www.giantbomb.com/[name]/[id]/
		link = request.POST.get('link')
		gb_id = link.partition(".com/")[2].partition("/")[2].partition("/")[0]
		api_key = os.environ['GBOMB_API_KEY']
		url = "https://www.giantbomb.com/api/game/" + gb_id + "/?api_key=" + api_key + "&format=JSON"
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
		success_url = '/items/games/' + str(game.id)
		return JsonResponse({'success_url': success_url})
	except:
		return JsonResponse({'error': 'Por favor, introduzca un enlace válido.'})

# DLC

class DLCDetail(DetailView):
	model = models.DLC
	template_name = 'items/game_detail.html'

	def get_context_data(self, **kwargs):
		context = super(DLCDetail, self).get_context_data(**kwargs)
		context['item_path'] = 'games/' + str(self.object.game.id)
		context['item_name'] = 'DLC'
		context['agents'] = group_agents(self.object.dlcinvolvement_set.all())
		context['mark_options'] = models.DLCMark.OPTION_CHOICES
		try:
			mark = self.request.user.dlcmark_set.get(dlc=self.object)
			context['mark'] = mark.option
			fav = mark.fav
			context['rate'] = mark.rating
		except models.DLCMark.DoesNotExist:
			fav = False
		context['fav'] = fav
		return context

class DLCCreate(CreateView):
	model = models.DLC
	form_class = forms.DLCForm
	template_name = 'items/item_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(DLCCreate, self).get_context_data(**kwargs)
		context['legend'] = "Nuevo DLC"
		context['cancel_url'] = "/items/games/" + str(self.kwargs['pk'])
		return context

	def form_valid(self, form):
		form.instance.game = models.Game.objects.get(pk=self.kwargs['pk'])
		return super(DLCCreate, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('items:dlc_detail', 
			kwargs={'pk': self.object.id})

class DLCUpdate(UpdateView):
	model = models.DLC
	form_class = forms.DLCForm
	template_name = 'items/item_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(DLCUpdate, self).get_context_data(**kwargs)
		context['legend'] = "Editar DLC"
		context['cancel_url'] = "/items/dlcs/" + str(self.object.id)
		return context

	def get_success_url(self):
		return reverse_lazy('items:dlc_detail', 
			kwargs={'pk': self.object.id})

class DLCDelete(DeleteView):
	model = models.DLC
	context_object_name = 'item'
	template_name = 'items/item_delete.html'
	
	def get_context_data(self, **kwargs):
		context = super(DLCDelete, self).get_context_data(**kwargs)
		context['message'] = "el DLC"
		context['cancel_url'] = "/items/dlcs/" + str(self.object.id)
		return context

	def get_success_url(self):
		return reverse_lazy('items:game_detail', 
			kwargs={'pk': self.object.game.id})

def dlc_mark(request):
	user = request.user
	dlc_id = request.POST['id']
	try:
		mark = user.dlcmark_set.get(dlc__id=dlc_id)
	except models.DLCMark.DoesNotExist:
		mark = models.DLCMark()
		mark.user = user
		mark.dlc_id = dlc_id
	option = request.POST.get('option')
	if option == "not":
		mark.option = ""
	else:
		mark.option = option
		# Log creation
		log = models.DLCMarkLog()
		log.user = user
		log.dlc_id = dlc_id
		log.option = option
		log.save()
	mark.save()
	return HttpResponse()

def dlc_fav(request):
	user = request.user
	dlc_id = request.POST['id']
	try:
		mark = user.dlcmark_set.get(dlc__id=dlc_id)
	except models.DLCMark.DoesNotExist:
		mark = models.DLCMark()
		mark.user = user
		mark.dlc_id = dlc_id
	fav = request.POST.get('fav')
	if fav == "unfav":
		fav = "fav"
		mark.fav = True
		# Log creation
		log = models.DLCMarkLog()
		log.user = user
		log.dlc_id = dlc_id
		log.fav = True
		log.save()
	elif fav == "fav":
		fav = "unfav"
		mark.fav = False
	mark.save()
	return HttpResponse(fav)

def dlc_rate(request):
	user = request.user
	dlc_id = request.POST['id']
	old_rating = None
	try:
		mark = user.dlcmark_set.get(dlc__id=dlc_id)
		old_rating = mark.rating
	except models.DLCMark.DoesNotExist:
		mark = models.DLCMark()
		mark.user = user
		mark.dlc_id = dlc_id
	new_rating = int(request.POST.get('rating'))
	mark.rating = new_rating
	mark.save()
	new_item_rating = update_item_rating(mark.dlc, old_rating, new_rating)
	# Log creation
	log = models.DLCMarkLog()
	log.user = user
	log.dlc_id = dlc_id
	log.rating = new_rating
	log.save()
	return HttpResponse(new_item_rating)

# Return involvements gruped by agent
def group_agents(involvements):
	agents = {}
	for i in involvements:
		if i.agent in agents:
			agents[i.agent].append(i.get_role_display())
		else:
			agents[i.agent] = [i.get_role_display(),]
	return agents

# Update item rating
def update_item_rating(item, old_rating, new_rating):
	old_sum = item.rating * item.count
	if old_rating:
		new_sum = old_sum + new_rating - old_rating
		item.rating = new_sum / item.count
	else:
		new_sum = old_sum + new_rating
		new_count = item.count + 1
		item.rating = new_sum / new_count
		item.count = new_count
	item.save()
	# Returns new item rating formatted to template
	new_item_rating = ('%.1f' % item.rating).replace('.', ',')
	return new_item_rating