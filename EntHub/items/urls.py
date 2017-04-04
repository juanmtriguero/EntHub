from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from items import views

urlpatterns = [
	url(r'^books$', login_required(views.book_list), name='book_list'),
	url(r'^books/(?P<pk>\d+)/', login_required(views.BookDetail.as_view()), name='book_detail'),
	url(r'^books/new$', login_required(views.BookCreate.as_view()), name='book_create'),
	url(r'^books/edit/(?P<pk>\d+)/', login_required(views.BookUpdate.as_view()), name='book_update'),
	url(r'^books/delete/(?P<pk>\d+)/', login_required(views.BookDelete.as_view()), name='book_delete'),
	url(r'^books/mark/', login_required(views.book_mark), name='book_mark'),
	url(r'^books/fav/', login_required(views.book_fav), name='book_fav'),
	url(r'^books/api/', login_required(views.book_api), name='book_api'),

	url(r'^movies$', login_required(views.movie_list), name='movie_list'),
	url(r'^movies/(?P<pk>\d+)/', login_required(views.MovieDetail.as_view()), name='movie_detail'),
	url(r'^movies/new$', login_required(views.MovieCreate.as_view()), name='movie_create'),
	url(r'^movies/edit/(?P<pk>\d+)/', login_required(views.MovieUpdate.as_view()), name='movie_update'),
	url(r'^movies/delete/(?P<pk>\d+)/', login_required(views.MovieDelete.as_view()), name='movie_delete'),
	url(r'^movies/mark/', login_required(views.movie_mark), name='movie_mark'),
	url(r'^movies/fav/', login_required(views.movie_fav), name='movie_fav'),
	url(r'^movies/api/', login_required(views.movie_api), name='movie_api'),

	url(r'^series$', login_required(views.series_list), name='series_list'),
	url(r'^series/(?P<pk>\d+)/', login_required(views.SeriesDetail.as_view()), name='series_detail'),
	url(r'^series/new$', login_required(views.SeriesCreate.as_view()), name='series_create'),
	url(r'^series/edit/(?P<pk>\d+)/', login_required(views.SeriesUpdate.as_view()), name='series_update'),
	url(r'^series/delete/(?P<pk>\d+)/', login_required(views.SeriesDelete.as_view()), name='series_delete'),
	url(r'^series/mark/', login_required(views.series_mark), name='series_mark'),
	url(r'^series/fav/', login_required(views.series_fav), name='series_fav'),
	url(r'^series/api/', login_required(views.series_api), name='series_api'),

	url(r'^chapter/add/(?P<pk>\d+)/', login_required(views.ChapterCreate.as_view()), name='add_chapter'),
	url(r'^chapter/tic/(?P<chapter_id>\d+)/', login_required(views.chapter_tic), name='chapter_tic'),
	url(r'^chapter/untic/(?P<chapter_id>\d+)/', login_required(views.chapter_untic), name='chapter_untic'),

	url(r'^comics$', login_required(views.comic_list), name='comic_list'),
	url(r'^comics/(?P<pk>\d+)/', login_required(views.ComicDetail.as_view()), name='comic_detail'),
	url(r'^comics/new$', login_required(views.ComicCreate.as_view()), name='comic_create'),
	url(r'^comics/edit/(?P<pk>\d+)/', login_required(views.ComicUpdate.as_view()), name='comic_update'),
	url(r'^comics/delete/(?P<pk>\d+)/', login_required(views.ComicDelete.as_view()), name='comic_delete'),
	url(r'^comics/mark/', login_required(views.comic_mark), name='comic_mark'),
	url(r'^comics/fav/', login_required(views.comic_fav), name='comic_fav'),

	url(r'^comicseries$', login_required(views.comic_series_list), name='comic_series_list'),
	url(r'^comicseries/(?P<pk>\d+)/', login_required(views.ComicSeriesDetail.as_view()), name='comic_series_detail'),
	url(r'^comicseries/new$', login_required(views.ComicSeriesCreate.as_view()), name='comic_series_create'),
	url(r'^comicseries/edit/(?P<pk>\d+)/', login_required(views.ComicSeriesUpdate.as_view()), name='comic_series_update'),
	url(r'^comicseries/delete/(?P<pk>\d+)/', login_required(views.ComicSeriesDelete.as_view()), name='comic_series_delete'),
	url(r'^comicseries/mark/', login_required(views.comic_series_mark), name='comic_series_mark'),
	url(r'^comicseries/fav/', login_required(views.comic_series_fav), name='comic_series_fav'),
	
	url(r'^number/add/(?P<pk>\d+)/', login_required(views.NumberCreate.as_view()), name='add_number'),
	url(r'^number/tic/(?P<number_id>\d+)/', login_required(views.number_tic), name='number_tic'),
	url(r'^number/untic/(?P<number_id>\d+)/', login_required(views.number_untic), name='number_untic'),

	url(r'^games$', login_required(views.game_list), name='game_list'),
	url(r'^games/(?P<pk>\d+)/', login_required(views.GameDetail.as_view()), name='game_detail'),
	url(r'^games/new$', login_required(views.GameCreate.as_view()), name='game_create'),
	url(r'^games/edit/(?P<pk>\d+)/', login_required(views.GameUpdate.as_view()), name='game_update'),
	url(r'^games/delete/(?P<pk>\d+)/', login_required(views.GameDelete.as_view()), name='game_delete'),
	url(r'^games/mark/', login_required(views.game_mark), name='game_mark'),
	url(r'^games/fav/', login_required(views.game_fav), name='game_fav'),

	url(r'^dlcs/(?P<pk>\d+)/', login_required(views.DLCDetail.as_view()), name='dlc_detail'),
	url(r'^dlcs/new/(?P<pk>\d+)/', login_required(views.DLCCreate.as_view()), name='dlc_create'),
	url(r'^dlcs/edit/(?P<pk>\d+)/', login_required(views.DLCUpdate.as_view()), name='dlc_update'),
	url(r'^dlcs/delete/(?P<pk>\d+)/', login_required(views.DLCDelete.as_view()), name='dlc_delete'),
	url(r'^dlcs/mark/', login_required(views.dlc_mark), name='dlc_mark'),
	url(r'^dlcs/fav/', login_required(views.dlc_fav), name='dlc_fav'),

	url(r'^search$', login_required(views.search), name='search'),
]