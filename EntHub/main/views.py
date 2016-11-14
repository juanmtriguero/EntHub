from django.shortcuts import render
from items.models import Game

def index(request):
    # TODO Contenido de prueba
    games = Game.objects.all()
    context = {'games': games}
    return render(request, 'main/index.html', context)