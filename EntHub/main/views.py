from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from items.models import Game
from main import models, forms

def index(request):
    # TODO Contenido de prueba
    games = Game.objects.all()
    context = {'games': games}
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
			account = models.Account()
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
		accounts = models.Account.objects.all()
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
	model = models.Account
	template_name = 'main/account_detail.html'

class AccountUpdate(UpdateView):
	model = models.Account
	form_class = forms.AccountForm
	template_name = 'main/account_form.html'
	
	def get_object(self):
		return self.request.user.account

	def get_success_url(self):
		return reverse_lazy('main:account_detail', 
			kwargs={'pk': self.object.id})
