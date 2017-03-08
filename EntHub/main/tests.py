from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Account
from items import models

# Index
class IndexTestCase(TestCase):

	fixtures = ['catalogue_test', 'users_test', 'marks_test']

	# Unregistered users are redirected to login
	def test_index_anonymous(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 302)
		redirect = self.client.get('/', follow=True)
		self.assertEqual(redirect.status_code, 200)
		self.assertTemplateUsed(redirect, 'main/login.html')

	# Index shows four last items of each category
	def test_index(self):
		self.client.login(username='anita', password='password')
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/index.html')
		# Context
		movies = [i.id for i in response.context['movies']]
		self.assertEqual(movies, [2,4,5,6])
		series = [i.id for i in response.context['series']]
		self.assertEqual(series, [1,2,3])
		books = [i.id for i in response.context['books']]
		self.assertEqual(books, [2,5,6,7])
		games = [i.id for i in response.context['games']]
		self.assertEqual(games, [1,2])
		comics = [i.id for i in response.context['comics']]
		self.assertEqual(comics, [1])
		comic_series = [i.id for i in response.context['comic_series']]
		self.assertEqual(comic_series, [1,2])

	# Items show user's marks
	def test_index_marks(self):
		self.client.login(username='jtorres', password='password')
		response = self.client.get('/')
		self.assertEqual(response.context['movies'][models.Movie.objects.get(id=5)], "pen")
		self.assertEqual(response.context['series'][models.Series.objects.get(id=2)], "fin")
		self.assertEqual(response.context['books'][models.Book.objects.get(id=6)], "lei")
		self.assertEqual(response.context['games'][models.Game.objects.get(id=1)], "jug")
		self.assertEqual(response.context['comics'][models.Comic.objects.get(id=1)], "ley")
		self.assertEqual(response.context['comic_series'][models.ComicSeries.objects.get(id=2)], "pau")

# Account
class AccountTestCase(TestCase):

	fixtures = ['users_test', 'accounts_test', 'catalogue_test', 'marks_test']

	# Account model
	def test_account_model(self):
		account = Account.objects.get(id=1)
		self.assertEqual(unicode(account), "admin")

	# Account detail
	def test_account_detail(self):
		self.client.login(username='anita', password='password')
		response = self.client.get('/accounts/2/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/account_detail.html')
		self.assertEqual([i.id for i in response.context['series']], [1])
		self.assertEqual([i.id for i in response.context['comicseries']], [1])
		self.assertEqual([i.id for i in response.context['books']], [5,7])
		self.assertEqual([i.id for i in response.context['comics']], [1])
		self.assertEqual([i.id for i in response.context['games']], [1])
		self.assertEqual([i.id for i in response.context['dlcs']], [3])

	# Account list
	def test_account_list(self):
		self.client.login(username='jtorres', password='password')
		# All accounts
		response = self.client.get('/accounts')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/account_list.html')
		self.assertEqual([i.id for i in response.context['accounts']], [1,2,3])
		self.assertEqual(response.context['q'], "")
		self.assertEqual(response.context['s'], "all")
		# Filter by search
		response = self.client.post('/accounts', {'q': 'adm'})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/account_list.html')
		self.assertEqual([i.id for i in response.context['accounts']], [1])
		self.assertEqual(response.context['q'], "adm")
		self.assertEqual(response.context['s'], "all")
		# Followers
		response = self.client.post('/accounts', {'s': 'fers'})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/account_list.html')
		self.assertEqual([i.id for i in response.context['accounts']], [3])
		self.assertEqual(response.context['q'], "")
		self.assertEqual(response.context['s'], "fers")
		# Following
		response = self.client.post('/accounts', {'s': 'fing'})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/account_list.html')
		self.assertEqual([i.id for i in response.context['accounts']], [1,3])
		self.assertEqual(response.context['q'], "")
		self.assertEqual(response.context['s'], "fing")
		# Mixed search
		response = self.client.post('/accounts', {'q': 'a', 's': 'fers'})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/account_list.html')
		self.assertEqual([i.id for i in response.context['accounts']], [3])
		self.assertEqual(response.context['q'], "a")
		self.assertEqual(response.context['s'], "fers")
		# Bad filtering
		response = self.client.post('/accounts', {'s': 'bad'})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/account_list.html')
		self.assertEqual(response.context['accounts'], None)
