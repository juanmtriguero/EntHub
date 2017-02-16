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
from main.models import Account

def index(request):
	movie_set = {}
	for movie in models.Movie.objects.all().order_by('id').reverse()[:4]:
		try:
			option = request.user.moviemark_set.get(movie=movie).option
		except models.MovieMark.DoesNotExist:
			option = None
		movie_set.update({movie: option})
	series_set = {}
	for series in models.Series.objects.all().order_by('id').reverse()[:4]:
		try:
			option = request.user.seriesmark_set.get(series=series).option
		except models.SeriesMark.DoesNotExist:
			option = None
		series_set.update({series: option})
	book_set = {}
	for book in models.Book.objects.all().order_by('id').reverse()[:4]:
		try:
			option = request.user.bookmark_set.get(book=book).option
		except models.BookMark.DoesNotExist:
			option = None
		book_set.update({book: option})
	game_set = {}
	for game in models.Game.objects.all().order_by('id').reverse()[:4]:
		try:
			option = request.user.gamemark_set.get(game=game).option
		except models.GameMark.DoesNotExist:
			option = None
		game_set.update({game: option})
	comic_set = {}
	for comic in models.Comic.objects.all().order_by('id').reverse()[:2]:
		try:
			option = request.user.comicmark_set.get(comic=comic).option
		except models.ComicMark.DoesNotExist:
			option = None
		comic_set.update({comic: option})
	comic_series_set = {}
	for comic_series in models.ComicSeries.objects.all().order_by('id').reverse()[:2]:
		try:
			option = request.user.comicseriesmark_set.get(comic=comic_series).option
		except models.ComicSeriesMark.DoesNotExist:
			option = None
		comic_series_set.update({comic_series: option})
	context = {'movies': movie_set, 'series': series_set, 'books': book_set,
			'games': game_set, 'comics': comic_set, 'comic_series': comic_series_set}
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