from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from items import models
from main import forms

def index(request):
    # TODO Contenido de prueba
    games = models.Game.objects.all()
    context = {'games': games}
    return render(request, 'main/index.html', context)

class AccountRegister(CreateView):
	model = models.Account
	template_name = 'main/register.html'
	form_class = forms.AccountForm
	second_form_class = forms.UserForm
	success_url = reverse_lazy('main:index')

	def get_context_data(self, **kwargs):
	    context = super(AccountRegister, self).get_context_data(**kwargs)
	    if 'form' not in context:
	    	context['form'] = self.form_class(self.request.GET)
	    if 'form2' not in context:
	    	context['form2'] = self.second_form_class(self.request.GET)
	    return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		form2 = self.second_form_class(request.POST)
		if form.is_valid() and form2.is_valid():
			account = form.save(commit=False)
			account.user = form2.save()
			account.save()
			user = authenticate(username=form2.cleaned_data['username'], \
				password=form2.cleaned_data['password1'])
			login(request, user)
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form, form2=form2))