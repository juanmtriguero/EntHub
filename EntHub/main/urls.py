from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login
from django.contrib.auth.decorators import login_required
from main import views

urlpatterns = [
	url(r'^$', login_required(views.index), name='index'),
    url(r'^accounts/login/', login, {'template_name': 'main/login.html'}, name='login'),
    url(r'^accounts/logout/', logout_then_login, name='logout'),
]