from django.shortcuts import render

# Create your views here.
from tournee.models import Players, Teams, GameScores, Tournaments, TournamentResult
from django.views import generic
from django.views.generic.list import ListView
from django.utils import timezone


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_tournaments = Tournaments.objects.all().count()
    num_players = Players.objects.all().count()

    # The 'all()' is implied by default.
    num_teams = Teams.objects.count()

    context = {
        'num_tournaments': num_tournaments,
        'num_players': num_players,
        'num_teams': num_teams,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class TournamentListView(ListView):
    model = Tournaments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class TournamentDetailView(generic.DetailView):
    model = Tournaments
