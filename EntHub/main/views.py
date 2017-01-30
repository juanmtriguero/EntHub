from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
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
		user.is_active = False
		user.save()
		return HttpResponseRedirect(reverse_lazy('main:logout'))