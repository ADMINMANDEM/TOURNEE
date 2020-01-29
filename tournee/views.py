from django.shortcuts import render

# Create your views here.
from tournee.models import Players, Teams, GameScores, Tournaments, TournamentResult


def index(request):
    return render(request, 'index.html')