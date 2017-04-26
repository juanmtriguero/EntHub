#encoding:utf-8

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from items import models
from main import forms
from main.models import Account, FollowingLog
import recommendations

def index(request):
	# Items recommended, lastest or best rated
	o = request.POST.get('option', 'rec')
	if o == "rec":
		movie_list = recommendations.recommended_movies(request.user, 4)
		series_list = recommendations.recommended_series(request.user, 4)
		book_list = recommendations.recommended_books(request.user, 4)
		game_list = recommendations.recommended_games(request.user, 4)
		comic_list = recommendations.recommended_comics(request.user, 4)
		comic_series_list = recommendations.recommended_comicseries(request.user, 4)
		prefix = "Te recomendamos"
	elif o == "nov":
		movie_list = models.Movie.objects.all().order_by('id').reverse()[:4]
		series_list = models.Series.objects.all().order_by('id').reverse()[:4]
		book_list = models.Book.objects.all().order_by('id').reverse()[:4]
		game_list = models.Game.objects.all().order_by('id').reverse()[:4]
		comic_list = models.Comic.objects.all().order_by('id').reverse()[:2]
		comic_series_list = models.ComicSeries.objects.all().order_by('id').reverse()[:2]
		prefix = "Lo último"
	elif o == "val":
		movie_list = models.Movie.objects.all().order_by('rating').reverse()[:4]
		series_list = models.Series.objects.all().order_by('rating').reverse()[:4]
		book_list = models.Book.objects.all().order_by('rating').reverse()[:4]
		game_list = models.Game.objects.all().order_by('rating').reverse()[:4]
		comic_list = models.Comic.objects.all().order_by('rating').reverse()[:2]
		comic_series_list = models.ComicSeries.objects.all().order_by('rating').reverse()[:2]
		prefix = "Lo mejor"
	# Adds user's marks to items
	movie_set = {}
	for movie in movie_list:
		try:
			option = request.user.moviemark_set.get(movie=movie).option
		except models.MovieMark.DoesNotExist:
			option = None
		movie_set.update({movie: option})
	series_set = {}
	for series in series_list:
		try:
			option = request.user.seriesmark_set.get(series=series).option
		except models.SeriesMark.DoesNotExist:
			option = None
		series_set.update({series: option})
	book_set = {}
	for book in book_list:
		try:
			option = request.user.bookmark_set.get(book=book).option
		except models.BookMark.DoesNotExist:
			option = None
		book_set.update({book: option})
	game_set = {}
	for game in game_list:
		try:
			option = request.user.gamemark_set.get(game=game).option
		except models.GameMark.DoesNotExist:
			option = None
		game_set.update({game: option})
	comic_set = {}
	for comic in comic_list:
		try:
			option = request.user.comicmark_set.get(comic=comic).option
		except models.ComicMark.DoesNotExist:
			option = None
		comic_set.update({comic: option})
	comic_series_set = {}
	for comic_series in comic_series_list:
		try:
			option = request.user.comicseriesmark_set.get(comic=comic_series).option
		except models.ComicSeriesMark.DoesNotExist:
			option = None
		comic_series_set.update({comic_series: option})
	# Logs
	logs = []
	for account in request.user.account.following.all():
		logs.extend(account.following_logs.all())
		logs.extend(account.user.bookmarklog_set.all())
		logs.extend(account.user.moviemarklog_set.all())
		logs.extend(account.user.seriesmarklog_set.all())
		logs.extend(account.user.comicmarklog_set.all())
		logs.extend(account.user.comicseriesmarklog_set.all())
		logs.extend(account.user.gamemarklog_set.all())
		logs.extend(account.user.dlcmarklog_set.all())
	logs.extend(request.user.account.following_logs.all())
	logs.extend(request.user.bookmarklog_set.all())
	logs.extend(request.user.moviemarklog_set.all())
	logs.extend(request.user.seriesmarklog_set.all())
	logs.extend(request.user.comicmarklog_set.all())
	logs.extend(request.user.comicseriesmarklog_set.all())
	logs.extend(request.user.gamemarklog_set.all())
	logs.extend(request.user.dlcmarklog_set.all())
	logs.sort(key=lambda log: log.date, reverse=True)
	# Context
	context = {'option': o, 'prefix': prefix, 'movies': movie_set,
			'series': series_set, 'books': book_set, 'games': game_set,
			'comics': comic_set, 'comic_series': comic_series_set, 'logs': logs[:15]}
	return render(request, 'main/index.html', context)

class UserRegister(CreateView):
	model = User
	template_name = 'main/register.html'
	form_class = forms.UserForm
	success_url = reverse_lazy('main:index')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		if form.is_valid():
			account = Account()
			account.user = form.save()
			account.save()
			user = authenticate(username=form.cleaned_data['username'], \
				password=form.cleaned_data['password1'])
			login(request, user)
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form))

def account_list(request):

	# Filter by status
	s = request.POST.get('s', 'all')
	acc = request.user.account
	if s == "all":
		accounts = Account.objects.all()
	elif s == "fers":
		accounts = acc.followers.all()
	elif s == "fing":
		accounts = acc.following.all()
	else:
		accounts = None

	# Filter by search
	q = request.POST.get('q', '')
	if q:
		accounts = accounts.filter(user__username__icontains=q)

	context = {'accounts': accounts, 'q': q, 's': s}
	return render(request, 'main/account_list.html', context)

class AccountDetail(DetailView):
	model = Account
	template_name = 'main/account_detail.html'

	def get_context_data(self, **kwargs):
		context = super(AccountDetail, self).get_context_data(**kwargs)
		user = self.object.user
		series_set = {}
		for series in [m.series for m in user.seriesmark_set.filter(option='sig')]:
			try:
				option = self.request.user.seriesmark_set.get(series=series).option
			except models.SeriesMark.DoesNotExist:
				option = None
			series_set.update({series: option})
		context['series'] = series_set
		comic_series_set = {}
		for comic_series in [m.comic for m in user.comicseriesmark_set.filter(option='sig')]:
			try:
				option = self.request.user.comicseriesmark_set.get(comic=comic_series).option
			except models.ComicSeriesMark.DoesNotExist:
				option = None
			comic_series_set.update({comic_series: option})
		context['comicseries'] = comic_series_set
		book_set = {}
		for book in [m.book for m in user.bookmark_set.filter(option='ley')]:
			try:
				option = self.request.user.bookmark_set.get(book=book).option
			except models.BookMark.DoesNotExist:
				option = None
			book_set.update({book: option})
		context['books'] = book_set
		comic_set = {}
		for comic in [m.comic for m in user.comicmark_set.filter(option='ley')]:
			try:
				option = self.request.user.comicmark_set.get(comic=comic).option
			except models.ComicMark.DoesNotExist:
				option = None
			comic_set.update({comic: option})
		context['comics'] = comic_set
		game_set = {}
		for game in [m.game for m in user.gamemark_set.filter(option='jug')]:
			try:
				option = self.request.user.gamemark_set.get(game=game).option
			except models.GameMark.DoesNotExist:
				option = None
			game_set.update({game: option})
		context['games'] = game_set
		dlc_set = {}
		for dlc in [m.dlc for m in user.dlcmark_set.filter(option='jug')]:
			try:
				option = self.request.user.dlcmark_set.get(dlc=dlc).option
			except models.DLCMark.DoesNotExist:
				option = None
			dlc_set.update({dlc: option})
		context['dlcs'] = dlc_set
		# Logs
		logs = []
		logs.extend(user.account.following_logs.all())
		logs.extend(user.bookmarklog_set.all())
		logs.extend(user.moviemarklog_set.all())
		logs.extend(user.seriesmarklog_set.all())
		logs.extend(user.comicmarklog_set.all())
		logs.extend(user.comicseriesmarklog_set.all())
		logs.extend(user.gamemarklog_set.all())
		logs.extend(user.dlcmarklog_set.all())
		logs.sort(key=lambda log: log.date, reverse=True)
		context['logs'] = logs[:15]
		return context

class AccountUpdate(UpdateView):
	model = Account
	second_model = User
	form_class = forms.AccountForm
	second_form_class = forms.UserNameForm
	template_name = 'main/account_form.html'

	def get_context_data(self, **kwargs):
		context = super(AccountUpdate, self).get_context_data(**kwargs)
		user = self.request.user
		if 'form' not in context:
			context['form'] = self.form_class()
		if 'form2' not in context:
			context['form2'] = self.second_form_class(instance=user)
		return context

	def get_object(self):
		return self.request.user.account

	def get_success_url(self):
		return reverse_lazy('main:account_detail', 
			kwargs={'pk': self.object.id})

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		user = request.user
		account = user.account
		form = self.form_class(request.POST, instance=account)
		form2 = self.second_form_class(request.POST, instance=user)
		if form.is_valid() and form2.is_valid():
			form.save()
			form2.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form, form2=form2))

def user_deactivate(request):
	if request.method == "GET":
		return render(request, 'main/user_deactivate.html')
	if request.method == "POST":
		user = request.user
		if user.check_password(request.POST['password']):
			user.is_active = False
			user.save()
			return HttpResponseRedirect(reverse_lazy('main:logout'))
		else:
			context = {'error': True}
			return render(request, 'main/user_deactivate.html', context)

def follow(request, account_id):
	my_account = request.user.account
	account = Account.objects.get(id=account_id)
	if my_account != account:
		my_account.following.add(account)
		# Log creation
		log = FollowingLog()
		log.follower = my_account
		log.following = account
		log.save()
		return HttpResponse()
	else:
		return HttpResponse(status=403)

def unfollow(request, account_id):
	my_account = request.user.account
	account = Account.objects.get(id=account_id)
	if my_account != account:
		my_account.following.remove(account)
		return HttpResponse()
	else:
		return HttpResponse(status=403)