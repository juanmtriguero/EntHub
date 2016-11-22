import math
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from items import models, forms

# Book

class BookList(ListView):
	model = models.Book
	template_name = 'items/book_list.html'

class BookDetail(DetailView):
	model = models.Book
	template_name = 'items/book_detail.html'

	def get_context_data(self, **kwargs):
	    context = super(BookDetail, self).get_context_data(**kwargs)
	    context['item_path'] = 'books'
	    context['item_name'] = 'Libro'
	    context['involvements'] = self.object.bookinvolvement_set.all()
	    return context

class BookCreate(CreateView):
	model = models.Book
	form_class = forms.BookForm
	template_name = 'items/book_create.html'
	success_url = reverse_lazy('items:book_list')

class BookUpdate(UpdateView):
	model = models.Book
	form_class = forms.BookForm
	template_name = 'items/book_update.html'
	
	def get_context_data(self, **kwargs):
		context = super(BookUpdate, self).get_context_data(**kwargs)
		context['cancel_url'] = "/items/books/" + unicode(self.object.id)
		return context

	def get_success_url(self):
		return reverse_lazy('items:book_detail', 
			kwargs={'pk': self.object.id})

class BookDelete(DeleteView):
	model = models.Book
	template_name = 'items/book_delete.html'
	success_url = reverse_lazy('items:book_list')

# Films & TV

class FilmTVList(ListView):
	model = models.Movie
	template_name = 'items/film_tv_list.html'
	context_object_name = 'movie_list'

	def get_context_data(self, **kwargs):
	    context = super(FilmTVList, self).get_context_data(**kwargs)
	    context['series_list'] = models.Series.objects.all()
	    return context