from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from items import views

urlpatterns = [
	url(r'^books$', login_required(views.BookList.as_view()), name='book_list'),
	url(r'^books/(?P<pk>\d+)/', login_required(views.BookDetail.as_view()), name='book_detail'),
	url(r'^books/new$', login_required(views.BookCreate.as_view()), name='book_create'),
	url(r'^books/edit/(?P<pk>\d+)/', login_required(views.BookUpdate.as_view()), name='book_update'),
	url(r'^books/delete/(?P<pk>\d+)/', login_required(views.BookDelete.as_view()), name='book_delete'),

	url(r'^movies$', login_required(views.FilmTVList.as_view()), name='film_tv_list'),
	url(r'^series$', login_required(views.FilmTVList.as_view()), name='film_tv_list'),
	url(r'^movies/(?P<pk>\d+)/', login_required(views.MovieDetail.as_view()), name='movie_detail'),
]