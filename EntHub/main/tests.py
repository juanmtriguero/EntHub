#encoding:utf-8

from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Account
from items import models
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

# Index
class IndexTestCase(TestCase):

	fixtures = ['catalogue_test', 'users_test', 'marks_test']

	# Unregistered users are redirected to login
	def test_index_anonymous(self):
		response = self.client.get('/')
		self.assertRedirects(response, '/accounts/login/?next=/')
		redirect = self.client.get('/', follow=True)
		self.assertTemplateUsed(redirect, 'main/login.html')

	# Registered users can access index
	def test_index(self):
		self.client.login(username='anita', password='password')
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/index.html')

	# 'Latest' shows four last items of each category
	def test_index_latest(self):
		self.client.login(username='anita', password='password')
		response = self.client.post('/', {'option': 'nov'})
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

	# 'Best rated' shows four best rated items of each category
	def test_index_best_rated(self):
		self.client.login(username='anita', password='password')
		response = self.client.post('/', {'option': 'val'})
		movies = [i.id for i in response.context['movies']]
		self.assertEqual(movies, [2,4,5,6])
		series = [i.id for i in response.context['series']]
		self.assertEqual(series, [1,2,3])
		books = [i.id for i in response.context['books']]
		self.assertEqual(books, [1,2,5,7])
		games = [i.id for i in response.context['games']]
		self.assertEqual(games, [1,2])
		comics = [i.id for i in response.context['comics']]
		self.assertEqual(comics, [1])
		comic_series = [i.id for i in response.context['comic_series']]
		self.assertEqual(comic_series, [1,2])

	# Items show user's marks
	def test_index_marks(self):
		self.client.login(username='jtorres', password='password')
		response = self.client.post('/', {'option': 'nov'})
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
		self.assertEqual([i.id for i in response.context['accounts']], [1])
		self.assertEqual(response.context['q'], "adm")
		self.assertEqual(response.context['s'], "all")
		# Followers
		response = self.client.post('/accounts', {'s': 'fers'})
		self.assertEqual([i.id for i in response.context['accounts']], [3])
		self.assertEqual(response.context['q'], "")
		self.assertEqual(response.context['s'], "fers")
		# Following
		response = self.client.post('/accounts', {'s': 'fing'})
		self.assertEqual([i.id for i in response.context['accounts']], [1,3])
		self.assertEqual(response.context['q'], "")
		self.assertEqual(response.context['s'], "fing")
		# Mixed search
		response = self.client.post('/accounts', {'q': 'a', 's': 'fers'})
		self.assertEqual([i.id for i in response.context['accounts']], [3])
		self.assertEqual(response.context['q'], "a")
		self.assertEqual(response.context['s'], "fers")
		# Bad filtering
		response = self.client.post('/accounts', {'s': 'bad'})
		self.assertEqual(response.context['accounts'], None)

	# Account update
	def test_account_update(self):
		self.client.login(username='anita', password='password')
		get_response = self.client.get('/accounts/edit/')
		self.assertEqual(get_response.status_code, 200)
		self.assertTemplateUsed(get_response, 'main/account_form.html')
		self.assertIn('form', get_response.context)
		self.assertIn('form2', get_response.context)
		form_data = {
			'first_name': 'Ana',
			'last_name': 'Espinosa Test',
			'birth': '1996-05-12',
			'text': 'Texto de prueba',
			'avatar': ''
		}
		post_response = self.client.post('/accounts/edit/', form_data, follow=True)
		self.assertRedirects(post_response, '/accounts/3/')
		user = User.objects.get(username='anita')
		self.assertEqual(user.last_name, 'Espinosa Test')
		self.assertEqual(user.account.text, 'Texto de prueba')

	# Account invalid update
	def test_account_invalid_update(self):
		self.client.login(username='anita', password='password')
		form_data = {
			'first_name': 'Ana',
			'last_name': 'Espinosa Test',
			'birth': '1996-05-12',
			'text': 'Texto de prueba',
			'avatar': 'not_url'
		}
		response = self.client.post('/accounts/edit/', form_data, follow=True)
		self.assertFormError(response, 'form', 'avatar', u'Introduzca una URL válida.')
		user = User.objects.get(username='anita')
		self.assertEqual(user.last_name, 'Espinosa')
		self.assertEqual(user.account.text, '')

# User
class UserTestCase(TestCase):

	fixtures = ['users_test']

	# User register
	def test_user_register(self):
		form_data = {
			'username': 'user',
			'first_name': 'Usuario',
			'last_name': 'De Ejemplo',
			'email': 'user@mail.com',
			'password1': 'password',
			'password2': 'password'
		}
		response = self.client.post('/accounts/register/', form_data, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/index.html')
		user = User.objects.get(username='user')
		self.assertIsNotNone(user.account)

	# User invalid register
	def test_user_invalid_register(self):
		form_data = {
			'username': '',
			'first_name': 'Usuario',
			'last_name': 'De Ejemplo',
			'email': 'user@mail.com',
			'password1': 'password',
			'password2': 'password'
		}
		response = self.client.post('/accounts/register/', form_data, follow=True)
		self.assertFormError(response, 'form', 'username', 'Este campo es obligatorio.')

	# User deactivate
	def test_user_deactivate(self):
		self.client.login(username='jtorres', password='password')
		response = self.client.get('/accounts/deactivate/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/user_deactivate.html')
		response = self.client.post('/accounts/deactivate/',
				{'password': 'password'}, follow=True)
		self.assertRedirects(response, '/accounts/login/')
		user = User.objects.get(username='jtorres')
		self.assertFalse(user.is_active)

	# User invalid deactivate
	def test_user_invalid_deactivate(self):
		self.client.login(username='jtorres', password='password')
		response = self.client.post('/accounts/deactivate/', {'password': 'false_password'})
		self.assertTemplateUsed(response, 'main/user_deactivate.html')
		self.assertTrue(response.context['error'])
		user = User.objects.get(username='jtorres')
		self.assertTrue(user.is_active)

# Follow & unfollow
class FollowingTestCase(TestCase):

	fixtures = ['users_test', 'accounts_test']

	def setUp(self):
		self.client.login(username='anita', password='password')

	# Follow user
	def test_follow(self):
		self.client.get('/accounts/follow/1/')
		account = Account.objects.get(id=1)
		self_account = Account.objects.get(id=3)
		self.assertIn(account, self_account.following.all())
		self.assertIn(self_account, account.followers.all())

	# Cannot follow itself
	def test_follow_self(self):
		response = self.client.get('/accounts/follow/3/')
		self.assertEqual(response.status_code, 403)

	# Unollow user
	def test_unfollow(self):
		self.client.get('/accounts/unfollow/2/')
		account = Account.objects.get(id=2)
		self_account = Account.objects.get(id=3)
		self.assertNotIn(account, self_account.following.all())
		self.assertNotIn(self_account, account.followers.all())

	# Cannot unfollow itself
	def test_unfollow_self(self):
		response = self.client.get('/accounts/unfollow/3/')
		self.assertEqual(response.status_code, 403)


# ACCEPTANCE TESTS

# Login 
class LoginAcceptanceTestCase(StaticLiveServerTestCase):

	fixtures = ['users_test']
	
	@classmethod
	def setUpClass(cls):
		super(LoginAcceptanceTestCase, cls).setUpClass()
		cls.selenium = WebDriver()
		cls.selenium.implicitly_wait(30)

	@classmethod
	def tearDownClass(cls):
		cls.selenium.quit()
		super(LoginAcceptanceTestCase, cls).tearDownClass()
	
	def test_acceptance_login(self):
		driver = self.selenium
		driver.get(self.live_server_url + "/accounts/login/")
		driver.find_element_by_css_selector("button.btn.btn-primary").click()
		self.assertEqual(u"Nombre de usuario\nEste campo es obligatorio.", driver.find_element_by_css_selector("div.form-group.has-error").text)
		self.assertEqual(u"Contraseña\nEste campo es obligatorio.", driver.find_element_by_xpath("//div[2]").text)
		driver.find_element_by_name("username").clear()
		driver.find_element_by_name("username").send_keys("not_user")
		driver.find_element_by_name("password").clear()
		driver.find_element_by_name("password").send_keys("not_password")
		driver.find_element_by_css_selector("button.btn.btn-primary").click()
		self.assertEqual(u"Por favor, introduce un nombre de usuario y clave correctos. Observa que ambos campos pueden ser sensibles a mayúsculas.", driver.find_element_by_css_selector("div.non-field-error-message").text)
		driver.find_element_by_name("username").clear()
		driver.find_element_by_name("username").send_keys("jtorres")
		driver.find_element_by_name("password").clear()
		driver.find_element_by_name("password").send_keys("password")
		driver.find_element_by_css_selector("button.btn.btn-primary").click()
		self.assertEqual(u"Lo último en cine", driver.find_element_by_css_selector("h2").text)
