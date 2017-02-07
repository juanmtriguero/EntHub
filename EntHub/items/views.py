#encoding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from items import models, forms

# Items catalogue

def catalogue(request):

	# Filter by category
	c = request.POST.get('c', 'books')
	if c == "books":
		items = models.Book.objects.all()
	elif c == "movies":
		items = models.Movie.objects.all()
	elif c == "series":
		items = models.Series.objects.all()
	elif c == "comics":
		items = models.Comic.objects.all()
	elif c == "comicseries":
		items = models.ComicSeries.objects.all()
	elif c == "games":
		items = models.Game.objects.all()
	else:
		items = None

	# Filter by search
	q = request.POST.get('q', '')
	if q:
		items = items.filter(title__icontains=q)

	context = {'items': items, 'q': q, 'c': c}
	return render(request, 'items/catalogue.html', context)

# Book

def book_list(request):
	# Filter by mark
	m = request.POST.get('m')
	if m:
		if m != 'fav':
			marks = request.user.bookmark_set.filter(option=m)
		else:
			marks = request.user.bookmark_set.filter(fav='True')
		items = [mark.book for mark in marks]
	else:
		items = models.Book.objects.all()
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
			fav = self.request.user.bookmark_set.get(book=self.object).fav
		except models.BookMark.DoesNotExist:
			fav = False
		context['fav'] = fav
		return context

class BookCreate(CreateView):
	model = models.Book
	form_class = forms.BookForm
	template_name = 'items/item_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(BookCreate, self).get_context_data(**kwargs)
		context['legend'] = "Nuevo libro"
		context['cancel_url'] = "/items/books"
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
		context['cancel_url'] = "/items/books/" + unicode(self.object.id)
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
		context['cancel_url'] = "/items/books/" + unicode(self.object.id)
		return context

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
	mark.fav = fav == "fav"
	mark.save()
	return HttpResponseRedirect(reverse_lazy('items:book_detail', 
			kwargs={'pk': book_id}))

# Movie

def movie_list(request):
	# Filter by mark
	m = request.POST.get('m')
	if m:
		if m != 'fav':
			marks = request.user.moviemark_set.filter(option=m)
		else:
			marks = request.user.moviemark_set.filter(fav='True')
		items = [mark.movie for mark in marks]
	else:
		items = models.Movie.objects.all()
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
			fav = self.request.user.moviemark_set.get(movie=self.object).fav
		except models.MovieMark.DoesNotExist:
			fav = False
		context['fav'] = fav
		return context

class MovieCreate(CreateView):
	model = models.Movie
	form_class = forms.MovieForm
	template_name = 'items/item_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(MovieCreate, self).get_context_data(**kwargs)
		context['legend'] = "Nueva película"
		context['cancel_url'] = "/items/movies"
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
		context['cancel_url'] = "/items/movies/" + unicode(self.object.id)
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
		context['cancel_url'] = "/items/movies/" + unicode(self.object.id)
		return context

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
	mark.fav = fav == "fav"
	mark.save()
	return HttpResponseRedirect(reverse_lazy('items:movie_detail', 
			kwargs={'pk': movie_id}))

# Series

def series_list(request):
	# Filter by mark
	m = request.POST.get('m')
	if m:
		if m != 'fav':
			marks = request.user.seriesmark_set.filter(option=m)
		else:
			marks = request.user.seriesmark_set.filter(fav='True')
		items = [mark.series for mark in marks]
	else:
		items = models.Series.objects.all()
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
			fav = self.request.user.seriesmark_set.get(series=self.object).fav
		except models.SeriesMark.DoesNotExist:
			fav = False
		context['fav'] = fav
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
	template_name = 'items/item_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(SeriesCreate, self).get_context_data(**kwargs)
		context['legend'] = "Nueva serie"
		context['cancel_url'] = "/items/series"
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
		context['cancel_url'] = "/items/series/" + unicode(self.object.id)
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
		context['cancel_url'] = "/items/series/" + unicode(self.object.id)
		return context

class ChapterCreate(CreateView):
	model = models.Chapter
	form_class = forms.ChapterForm
	template_name = 'items/item_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(ChapterCreate, self).get_context_data(**kwargs)
		context['legend'] = "Añadir capítulo"
		context['cancel_url'] = "/items/series/" + unicode(self.kwargs['pk'])
		return context

	def form_valid(self, form):
		form.instance.series = models.Series.objects.get(pk=self.kwargs['pk'])
		return super(ChapterCreate, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('items:series_detail', 
			kwargs={'pk': self.kwargs['pk']})

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
	mark.fav = fav == "fav"
	mark.save()
	return HttpResponseRedirect(reverse_lazy('items:series_detail', 
			kwargs={'pk': series_id}))

# Comic

def comic_list(request):
	# Filter by mark
	m = request.POST.get('m')
	if m:
		if m != 'fav':
			marks = request.user.comicmark_set.filter(option=m)
		else:
			marks = request.user.comicmark_set.filter(fav='True')
		items = [mark.comic for mark in marks]
	else:
		items = models.Comic.objects.all()
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
			fav = self.request.user.comicmark_set.get(comic=self.object).fav
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
		context['cancel_url'] = "/items/comics/" + unicode(self.object.id)
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
		context['cancel_url'] = "/items/comics/" + unicode(self.object.id)
		return context

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
	mark.fav = fav == "fav"
	mark.save()
	return HttpResponseRedirect(reverse_lazy('items:comic_detail', 
			kwargs={'pk': comic_id}))

# ComicSeries

def comic_series_list(request):
	# Filter by mark
	m = request.POST.get('m')
	if m:
		if m != 'fav':
			marks = request.user.comicseriesmark_set.filter(option=m)
		else:
			marks = request.user.comicseriesmark_set.filter(fav='True')
		items = [mark.comic for mark in marks]
	else:
		items = models.ComicSeries.objects.all()
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
			fav = self.request.user.comicseriesmark_set.get(comic=self.object).fav
		except models.ComicSeriesMark.DoesNotExist:
			fav = False
		context['fav'] = fav
		return context

class ComicSeriesCreate(CreateView):
	model = models.ComicSeries
	form_class = forms.ComicSeriesForm
	template_name = 'items/item_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(ComicSeriesCreate, self).get_context_data(**kwargs)
		context['legend'] = "Nueva serie de cómics"
		context['cancel_url'] = "/items/comicseries"
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
		context['cancel_url'] = "/items/comicseries/" + unicode(self.object.id)
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
		context['cancel_url'] = "/items/comicseries/" + unicode(self.object.id)
		return context

class NumberCreate(CreateView):
	model = models.Number
	form_class = forms.NumberForm
	template_name = 'items/item_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(NumberCreate, self).get_context_data(**kwargs)
		context['legend'] = "Añadir número"
		context['cancel_url'] = "/items/comicseries/" + unicode(self.kwargs['pk'])
		return context

	def form_valid(self, form):
		form.instance.comic = models.ComicSeries.objects.get(pk=self.kwargs['pk'])
		return super(NumberCreate, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('items:comic_series_detail', 
			kwargs={'pk': self.kwargs['pk']})

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
	mark.fav = fav == "fav"
	mark.save()
	return HttpResponseRedirect(reverse_lazy('items:comic_series_detail', 
			kwargs={'pk': comic_id}))

# Game

def game_list(request):
	# Filter by mark
	m = request.POST.get('m')
	if m:
		if m != 'fav':
			marks = request.user.gamemark_set.filter(option=m)
		else:
			marks = request.user.gamemark_set.filter(fav='True')
		items = [mark.game for mark in marks]
	else:
		items = models.Game.objects.all()
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
			fav = self.request.user.gamemark_set.get(game=self.object).fav
		except models.GameMark.DoesNotExist:
			fav = False
		context['fav'] = fav
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
	template_name = 'items/item_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(GameCreate, self).get_context_data(**kwargs)
		context['legend'] = "Nuevo videojuego"
		context['cancel_url'] = "/items/games"
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
		context['cancel_url'] = "/items/games/" + unicode(self.object.id)
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
		context['cancel_url'] = "/items/games/" + unicode(self.object.id)
		return context

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
	mark.fav = fav == "fav"
	mark.save()
	return HttpResponseRedirect(reverse_lazy('items:game_detail', 
			kwargs={'pk': game_id}))

# DLC

class DLCDetail(DetailView):
	model = models.DLC
	template_name = 'items/game_detail.html'

	def get_context_data(self, **kwargs):
		context = super(DLCDetail, self).get_context_data(**kwargs)
		context['item_path'] = 'games/' + unicode(self.object.game.id)
		context['item_name'] = 'DLC'
		context['agents'] = group_agents(self.object.dlcinvolvement_set.all())
		context['mark_options'] = models.DLCMark.OPTION_CHOICES
		try:
			fav = self.request.user.dlcmark_set.get(dlc=self.object).fav
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
		context['cancel_url'] = "/items/games/" + unicode(self.kwargs['pk'])
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
		context['cancel_url'] = "/items/dlcs/" + unicode(self.object.id)
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
		context['cancel_url'] = "/items/dlcs/" + unicode(self.object.id)
		return context

	def get_success_url(self):
		return reverse_lazy('items:game_detail', 
			kwargs={'pk': self.object.game.id})

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
	mark.fav = fav == "fav"
	mark.save()
	return HttpResponseRedirect(reverse_lazy('items:dlc_detail', 
			kwargs={'pk': dlc_id}))

# Return involvements gruped by agent
def group_agents(involvements):
	agents = {}
	for i in involvements:
		if i.agent in agents:
			agents[i.agent].append(i.get_role_display())
		else:
			agents[i.agent] = [i.get_role_display(),]
	return agents