#encoding:utf-8

from django.db import models

# Genre

class Genre(models.Model):
	name = models.CharField(max_length=20)

	def __unicode__(self):
		return unicode(self.name)

# Agent

class Agent(models.Model):
	name = models.CharField(max_length=50)
	bio = models.TextField(blank=True)
	image = models.URLField(blank=True)

	def __unicode__(self):
		return unicode(self.name)

# Platform

class Platform(models.Model):
	name = models.CharField(max_length=50)
	short = models.CharField(max_length=5)
	image = models.URLField(blank=True)

	def __unicode__(self):
		return unicode(self.name)


'''
# Items

class Item(models.Model):
	title = models.CharField(max_length=100)
	year = models.IntegerField()
	description = models.TextField(blank=True)
	image = models.URLField(blank=True)
	rating = models.FloatField(default=0.0)
	count = models.IntegerField(default=0)
	genres = models.ManyToManyField(Genre)
	lists = models.ManyToManyField("List", blank=True)

	class Meta:
		abstract = True

	def __unicode__(self):
		return unicode(self.title) + " ("\
			   + unicode(self.year) + ")"

class Book(Item):
	persons = models.ManyToManyField(Agent, through="BookInvolvement")

# Sub-items

# TODO

# Marks

class Mark(models.Model):
	rating = fields.IntegerRangeField(blank=True, null=True, min_value=1, max_value=5)
	fav = models.BooleanField(default=False)

	class Meta:
		abstract = True

class BookMark(Mark):
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	OPTION_CHOICES = (
		('lei', 'leído'),
		('pen', 'pendiente'),
		('ley', 'leyendo'),
	)
	option = models.CharField(max_length=3, choices=OPTION_CHOICES)

	def __unicode__(self):
		return unicode(self.user) + " ha marcado el libro "\
			   + unicode(self.book) + " como " + unicode(self.get_option_display())

# Involvements

class BookInvolvement(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
	ROLE_CHOICES = (
		('esc', 'escritor'),
		('ilu', 'ilustrador'),
	)
	role = models.CharField(max_length=3, choices=ROLE_CHOICES)

	def __unicode__(self):
		return unicode(self.agent) + " aparece en el libro "\
			   + unicode(self.book) + " como " + unicode(self.get_role_display())

#List

class List(models.Model):
	name = models.CharField(max_length=100)
	creator = models.ForeignKey(Account, related_name="creator", on_delete=models.CASCADE)
	followers = models.ManyToManyField(Account, related_name="follower", blank=True)

	def __unicode__(self):
		return unicode(self.name)

'''