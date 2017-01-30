from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login, password_change
from django.contrib.auth.decorators import login_required
from main import views

urlpatterns = [
	url(r'^$', login_required(views.index), name='index'),
    url(r'^accounts/login/', login, {'template_name': 'main/login.html'}, name='login'),
    url(r'^accounts/logout/', logout_then_login, name='logout'),
    url(r'^accounts/register/', views.UserRegister.as_view(), name='register'),

    url(r'^accounts$', login_required(views.account_list), name='account_list'),
	url(r'^accounts/(?P<pk>\d+)/', login_required(views.AccountDetail.as_view()), name='account_detail'),
    url(r'^accounts/edit/', login_required(views.AccountUpdate.as_view()), name='account_update'),
    url(r'^accounts/password/', login_required(password_change), {'template_name': 'main/password_change.html',
    		'post_change_redirect': 'main:account_update'}, name='password_change'),
    url(r'^accounts/deactivate/', login_required(views.user_deactivate), name='user_deactivate'),
]