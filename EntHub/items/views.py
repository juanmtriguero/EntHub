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
