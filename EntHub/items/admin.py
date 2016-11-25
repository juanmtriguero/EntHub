from django.contrib import admin
import items.models as models

admin.site.register(models.Genre)
admin.site.register(models.Agent)
admin.site.register(models.Platform)
admin.site.register(models.List)

admin.site.register(models.Book)

admin.site.register(models.Game)
admin.site.register(models.DLC)

admin.site.register(models.Comic)
admin.site.register(models.ComicSeries)

admin.site.register(models.Movie)
admin.site.register(models.Series)

admin.site.register(models.Number)
admin.site.register(models.Chapter)

admin.site.register(models.BookMark)
admin.site.register(models.GameMark)
admin.site.register(models.DLCMark)
admin.site.register(models.ComicMark)
admin.site.register(models.ComicSeriesMark)
admin.site.register(models.SeriesMark)
admin.site.register(models.MovieMark)

admin.site.register(models.BookInvolvement)
admin.site.register(models.GameInvolvement)
admin.site.register(models.DLCInvolvement)
admin.site.register(models.ComicInvolvement)
admin.site.register(models.ComicSeriesInvolvement)
admin.site.register(models.SeriesInvolvement)
admin.site.register(models.MovieInvolvement)