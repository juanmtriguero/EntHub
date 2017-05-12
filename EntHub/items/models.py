#encoding:utf-8

from django.db import models
from django.contrib.auth.models import User

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

#List

class List(models.Model):
	name = models.CharField(max_length=100)
	creator = models.ForeignKey(User, related_name="creator", on_delete=models.CASCADE)
	followers = models.ManyToManyField(User, related_name="follower", blank=True)

	def __unicode__(self):
		return unicode(self.name)

# Items

class Item(models.Model):
	title = models.CharField(max_length=100)
	year = models.IntegerField()
	description = models.TextField(blank=True)
	image = models.URLField(blank=True)
	rating = models.FloatField(default=0.0)
	count = models.IntegerField(default=0)
	genres = models.ManyToManyField(Genre, blank=True)
	lists = models.ManyToManyField(List, blank=True)

	class Meta:
		abstract = True

	def __unicode__(self):
		return unicode(self.title) + " ("\
			   + unicode(self.year) + ")"

class Book(Item):
	agents = models.ManyToManyField(Agent, through="BookInvolvement")

class GameItem(Item):
	platforms = models.ManyToManyField(Platform, blank=True)

	class Meta:
		abstract = True

class Game(GameItem):
	agents = models.ManyToManyField(Agent, through="GameInvolvement")

class DLC(GameItem):
	agents = models.ManyToManyField(Agent, through="DLCInvolvement")
	game = models.ForeignKey(Game, on_delete=models.CASCADE)

class Comic(Item):
	agents = models.ManyToManyField(Agent, through="ComicInvolvement")

class ComicSeries(Item):
	agents = models.ManyToManyField(Agent, through="ComicSeriesInvolvement")

class Movie(Item):
	CATEGORY_CHOICES = (
		('pel', 'Película'),
		('cor', 'Corto'),
		('doc', 'Docufilm'),
	)
	category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default='pel')
	duration = models.IntegerField()
	agents = models.ManyToManyField(Agent, through="MovieInvolvement")

class Series(Item):
	CATEGORY_CHOICES = (
		('ser', 'Serie'),
		('min', 'Miniserie'),
		('pro', 'Programa TV'),
		('doc', 'Documental'),
	)
	category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default='ser')
	STATUS_CHOICES = (
		('emi', 'En emisión'),
		('can', 'Cancelado'),
		('fin', 'Finalizado'),
		('esp', 'A espera de nueva temporada'),
	)
	status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='emi')
	agents = models.ManyToManyField(Agent, through="SeriesInvolvement")

# Sub-items

class Subitem(models.Model):
	number = models.IntegerField()
	name = models.CharField(max_length=100)
	tics = models.ManyToManyField(User, blank=True)

	class Meta:
		abstract = True

class Number(Subitem):
	comic = models.ForeignKey(ComicSeries, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.comic) + " - " + unicode(self.number)\
			   + ": " + unicode(self.name)

class Chapter(Subitem):
	season = models.IntegerField()
	series = models.ForeignKey(Series, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.series) + " - " + unicode(self.season)\
			   + "x" + unicode(self.number) + ": " + unicode(self.name)

# Marks

class Mark(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	rating = models.IntegerField(null=True, blank=True, choices=
		[(i, i) for i in range(1,6)])
	fav = models.BooleanField(default=False)

	class Meta:
		abstract = True

class IndividualMark(Mark):
	OPTION_CHOICES = (
		('pen', 'Pendiente'),
		('ley', 'Leyendo'),
		('pau', 'Pausado'),
		('lei', 'Leído'),
	)
	option = models.CharField(max_length=3, choices=OPTION_CHOICES, blank=True)

	class Meta:
		abstract = True

class BookMark(IndividualMark):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.user) + " ha marcado el libro "\
			   + unicode(self.book) + " como " + unicode(self.get_option_display())

class PlayableMark(Mark):
	OPTION_CHOICES = (
		('pen', 'Pendiente'),
		('jug', 'Jugando'),
		('pau', 'Pausado'),
		('ter', 'Terminado'),
		('com', 'Completado'),
	)
	option = models.CharField(max_length=3, choices=OPTION_CHOICES, blank=True)

	class Meta:
		abstract = True

class GameMark(PlayableMark):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.user) + " ha marcado el juego "\
			   + unicode(self.game) + " como " + unicode(self.get_option_display())

class DLCMark(PlayableMark):
	dlc = models.ForeignKey(DLC, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.user) + " ha marcado el DLC "\
			   + unicode(self.dlc) + " como " + unicode(self.get_option_display())

class ComicMark(IndividualMark):
	comic = models.ForeignKey(Comic, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.user) + u" ha marcado el cómic "\
			   + unicode(self.comic) + " como " + unicode(self.get_option_display())

class GroupMark(Mark):
	OPTION_CHOICES = (
		('pen', 'Pendiente'),
		('sig', 'Siguiendo'),
		('pau', 'Pausado'),
		('fin', 'Finalizado'),
	)
	option = models.CharField(max_length=3, choices=OPTION_CHOICES, blank=True)

	class Meta:
		abstract = True

class ComicSeriesMark(GroupMark):
	comic = models.ForeignKey(ComicSeries, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.user) + u" ha marcado la serie de cómics "\
			   + unicode(self.comic) + " como " + unicode(self.get_option_display())

class SeriesMark(GroupMark):
	series = models.ForeignKey(Series, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.user) + " ha marcado el " + unicode(self.series.get_category_display())\
			   + " " + unicode(self.series) + " como " + unicode(self.get_option_display())

class MovieMark(Mark):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	OPTION_CHOICES = (
		('pen', 'Pendiente'),
		('vis', 'Visto'),
	)
	option = models.CharField(max_length=3, choices=OPTION_CHOICES, blank=True)

	def __unicode__(self):
		return unicode(self.user) + " ha marcado el " + unicode(self.movie.get_category_display())\
			   + " " + unicode(self.movie) + " como " + unicode(self.get_option_display())

# Involvements

class Involvement(models.Model):
	agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

	class Meta:
		abstract = True

class BookInvolvement(Involvement):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	ROLE_CHOICES = (
		('esc', 'Escritor'),
		('ilu', 'Ilustrador'),
		('tra', 'Traductor'),
		('edi', 'Editorial'),
	)
	role = models.CharField(max_length=3, choices=ROLE_CHOICES)

	def __unicode__(self):
		return unicode(self.agent) + " aparece en el libro "\
			   + unicode(self.book) + " como " + unicode(self.get_role_display())

class GameItemInvolvement(Involvement):
	ROLE_CHOICES = (
		('des', 'Desarrollador'),
		('dis', 'Distribuidor'),
	)
	role = models.CharField(max_length=3, choices=ROLE_CHOICES)

	class Meta:
		abstract = True

class GameInvolvement(GameItemInvolvement):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.agent) + " aparece en el juego "\
			   + unicode(self.game) + " como " + unicode(self.get_role_display())

class DLCInvolvement(GameItemInvolvement):
	dlc = models.ForeignKey(DLC, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.agent) + " aparece en el DLC "\
			   + unicode(self.dlc) + " como " + unicode(self.get_role_display())

class ComicItemInvolvement(Involvement):
	ROLE_CHOICES = (
		('edi', 'Editorial'),
		('gui', 'Guionista'),
		('dib', 'Dibujante'),
	)
	role = models.CharField(max_length=3, choices=ROLE_CHOICES)

	class Meta:
		abstract = True

class ComicInvolvement(ComicItemInvolvement):
	comic = models.ForeignKey(Comic, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.agent) + u" aparece en el cómic "\
			   + unicode(self.comic) + " como " + unicode(self.get_role_display())

class ComicSeriesInvolvement(ComicItemInvolvement):
	comic = models.ForeignKey(ComicSeries, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.agent) + u" aparece en la serie de cómics "\
			   + unicode(self.comic) + " como " + unicode(self.get_role_display())

class MovieItemInvolvement(Involvement):
	ROLE_CHOICES = (
		('pra', 'Productora'),
		('dis', 'Distribuidora'),
		('pro', 'Productora'),
		('dir', 'Director'),
		('gui', 'Guionista'),
		('act', 'Actor'),
		('pre', 'Presentador'),
	)
	role = models.CharField(max_length=3, choices=ROLE_CHOICES)

	class Meta:
		abstract = True

class MovieInvolvement(MovieItemInvolvement):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.agent) + " aparece en " + unicode(self.movie.get_category_display())\
			   + " " + unicode(self.movie) + " como " + unicode(self.get_role_display())

class SeriesInvolvement(MovieItemInvolvement):
	series = models.ForeignKey(Series, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.agent) + " aparece en " + unicode(self.series.get_category_display())\
			   + " " + unicode(self.series) + " como " + unicode(self.get_role_display())

# Logs

class BookMarkLog(IndividualMark):
	date = models.DateTimeField(auto_now_add=True)
	book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='+')

	def __unicode__(self):
		return unicode(self.user) + " ha marcado el libro "\
			   + unicode(self.book) + " como " + unicode(self.get_option_display())

class MovieMarkLog(Mark):
	date = models.DateTimeField(auto_now_add=True)
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='+')
	OPTION_CHOICES = (
		('pen', 'Pendiente'),
		('vis', 'Visto'),
	)
	option = models.CharField(max_length=3, choices=OPTION_CHOICES, blank=True)

	def __unicode__(self):
		return unicode(self.user) + " ha marcado el " + unicode(self.movie.get_category_display())\
			   + " " + unicode(self.movie) + " como " + unicode(self.get_option_display())

class SeriesMarkLog(GroupMark):
	date = models.DateTimeField(auto_now_add=True)
	series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='+')

	def __unicode__(self):
		return unicode(self.user) + " ha marcado el " + unicode(self.series.get_category_display())\
			   + " " + unicode(self.series) + " como " + unicode(self.get_option_display())

class ComicMarkLog(IndividualMark):
	date = models.DateTimeField(auto_now_add=True)
	comic = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name='+')

	def __unicode__(self):
		return unicode(self.user) + u" ha marcado el cómic "\
			   + unicode(self.comic) + " como " + unicode(self.get_option_display())

class ComicSeriesMarkLog(GroupMark):
	date = models.DateTimeField(auto_now_add=True)
	comicseries = models.ForeignKey(ComicSeries, on_delete=models.CASCADE, related_name='+')

	def __unicode__(self):
		return unicode(self.user) + u" ha marcado la serie de cómics "\
			   + unicode(self.comic) + " como " + unicode(self.get_option_display())

class GameMarkLog(PlayableMark):
	date = models.DateTimeField(auto_now_add=True)
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='+')

	def __unicode__(self):
		return unicode(self.user) + " ha marcado el juego "\
			   + unicode(self.game) + " como " + unicode(self.get_option_display())

class DLCMarkLog(PlayableMark):
	date = models.DateTimeField(auto_now_add=True)
	dlc = models.ForeignKey(DLC, on_delete=models.CASCADE, related_name='+')

	def __unicode__(self):
		return unicode(self.user) + " ha marcado el DLC "\
			   + unicode(self.dlc) + " como " + unicode(self.get_option_display())