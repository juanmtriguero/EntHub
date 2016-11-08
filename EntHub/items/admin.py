from django.contrib import admin
import items.models as models

admin.site.register(models.Genre)
admin.site.register(models.Agent)
admin.site.register(models.Platform)
admin.site.register(models.List)

admin.site.register(models.Book)

admin.site.register(models.Game)
admin.site.register(models.DLC)

admin.site.register(models.GraphicNovel)
admin.site.register(models.Comic)

admin.site.register(models.Number)

admin.site.register(models.BookMark)
admin.site.register(models.GameMark)
admin.site.register(models.DLCMark)
admin.site.register(models.GraphicNovelMark)
admin.site.register(models.ComicMark)

admin.site.register(models.BookInvolvement)
admin.site.register(models.GameInvolvement)
admin.site.register(models.DLCInvolvement)
admin.site.register(models.GraphicNovelInvolvement)
admin.site.register(models.ComicInvolvement)