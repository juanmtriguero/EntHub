from django.shortcuts import render
from items import models

def index(request):
    # TODO Contenido de prueba
    games = models.Game.objects.all()
    context = {'games': games}
    return render(request, 'main/index.html', context)