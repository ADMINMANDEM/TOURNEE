from django.contrib import admin
from .models import Players, Teams, Tournaments, TournamentResult, GameScores

admin.site.register(Players)
admin.site.register(Teams)
admin.site.register(Tournaments)
admin.site.register(TournamentResult)
admin.site.register(GameScores)

