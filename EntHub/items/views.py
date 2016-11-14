from django.shortcuts import render
from items import models
from django.views.generic import ListView

# Book

class BookList(ListView):
	model = models.Book
	template_name = 'items/book_list.html'