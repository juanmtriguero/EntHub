from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Account

# main.views.index
class IndexTestCase(TestCase):

	def setUp(self):
		user = User.objects.create_user('user', 'user@mail.com', 'user')

	# Unregistered users are redirected to login
	def test_unregistered_index(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 302)
		redirect = self.client.get('/', follow=True)
		self.assertEqual(redirect.status_code, 200)
		self.assertTemplateUsed(redirect, 'main/login.html')

	# Registered users go to index
	def test_registered_index(self):
		self.client.login(username='user', password='user')
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/index.html')

# main.models
class ModelsTestCase(TestCase):

	fixtures = ['users', 'accounts']

	# models.Account
	def test_account_unicode(self):
		account = Account.objects.get(id=1)
		self.assertEqual(unicode(account), "admin")
