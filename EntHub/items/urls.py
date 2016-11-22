from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from items import views

urlpatterns = [
	url(r'^books$', login_required(views.BookList.as_view()), name='book_list'),
	url(r'^books/(?P<pk>\d+)/', login_required(views.BookDetail.as_view()), name='book_detail'),
	url(r'^books/new$', login_required(views.BookCreate.as_view()), name='book_create'),
	url(r'^books/edit/(?P<pk>\d+)/', login_required(views.BookUpdate.as_view()), name='book_update'),
	url(r'^books/delete/(?P<pk>\d+)/', login_required(views.BookDelete.as_view()), name='book_delete'),

	url(r'^movies$', login_required(views.FilmTVList.as_view()), name='movie_list'),
	url(r'^movies/(?P<pk>\d+)/', login_required(views.MovieDetail.as_view()), name='movie_detail'),
	url(r'^movies/new$', login_required(views.MovieCreate.as_view()), name='movie_create'),
	url(r'^movies/edit/(?P<pk>\d+)/', login_required(views.MovieUpdate.as_view()), name='movie_update'),
	url(r'^movies/delete/(?P<pk>\d+)/', login_required(views.MovieDelete.as_view()), name='movie_delete'),

	url(r'^series$', login_required(views.FilmTVList.as_view()), name='series_list'),
	url(r'^series/(?P<pk>\d+)/', login_required(views.SeriesDetail.as_view()), name='series_detail'),
]