from django.conf.urls import url
from items import views

urlpatterns = [
	url(r'^books$', views.BookList.as_view(), name='book_list'),
	url(r'^books/new$', views.BookCreate.as_view(), name='book_create'),
	url(r'^books/edit/(?P<pk>\d+)/$', views.BookUpdate.as_view(), name='book_update'),
	url(r'^books/delete/(?P<pk>\d+)/$', views.BookDelete.as_view(), name='book_delete'),
]