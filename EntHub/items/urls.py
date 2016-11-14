from django.conf.urls import url
from items import views

urlpatterns = [
	url(r'^books$', views.BookList.as_view(), name='books_list'),
]