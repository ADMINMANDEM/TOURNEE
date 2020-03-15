# Create your views here.

from tournee.models import Player, Team, Tournament, Seed
from django.views import generic
from django.utils import timezone
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from tournee.forms import *
from django.contrib import messages
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.views.generic.edit import ModelFormMixin

def index(request):
    # View function for home page of site.

    # Generate counts of the objects in tournaments, players and team
    num_tournaments = Tournament.objects.all().count()
    num_players = Player.objects.all().count()
    num_teams = Team.objects.count()

    context = {
        'num_tournaments': num_tournaments,
        'num_players': num_players,
        'num_teams': num_teams,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


# This is the definition for how my list of tournament will work
class TournamentListView(generic.ListView):
    # It uses the model Tournament
    model = Tournament
    # This determines how many items per page will be displayed
    paginate_by = 5


# This defines the detail page which lets the user see more information about the tournament
class TournamentDetailView(generic.DetailView):
    model = Tournament


class PlayerListView(generic.ListView):
    model = Player
    paginate_by = 5


class PlayerDetailView(generic.DetailView):
    model = Player


class TeamListView(generic.ListView):
    model = Team
    paginate_by = 5


class TeamDetailView(generic.DetailView):
    model = Team


# This defines the sign up process. This uses the inbuilt authentication system
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/profile/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# This is for the profile and choosing your teams. It combines the forms player and user so the user can
# customise how they appear to others
# @login_required means this page can't be accessed unless the user logs in
@login_required
@transaction.atomic
def update_player(request):
    if request.method == 'POST':
        # Tells function where to look for input from
        user_form = UserForm(request.POST, instance=request.user)
        player_form = PlayerForm(request.POST, instance=request.user.player)
        # Checks if form is valid then saves data if it is.
        if user_form.is_valid() and player_form.is_valid():
            user_form.save()
            player_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        player_form = PlayerForm(instance=request.user.player)
    # Tell program what html page to sow
    return render(request, 'registration/profile.html', {
        'user_form': user_form,
        'player_form': player_form
    })


# THis is the function behind the tournament form
@login_required
def create_tournament(request):
    tournament_form = TournamentForm(request.POST or None)
    if tournament_form.is_valid():
        # This means the tournament doesn't save until we've determined the captain
        tournament = tournament_form.save(commit=False)
        tournament.creatorid = Player.objects.get(account=request.user.id)
        tournament.save()
        # This part is more complex as it takes the many-to-many dropdown input and saves it as a new Seed record
        for team in tournament_form.cleaned_data['teams'].all():
            Seed.objects.create(tournament_id=tournament.id, team_id=team.id)
        messages.success(request, 'Your tournament was successfully created!')
        return redirect('Tournament/')
    else:
        messages.error(request, 'Please correct the error below.')
    return render(request, 'tournee/tournament_creation.html', {
        'tournament_form': tournament_form,
    })


# Function for team making form
@login_required
def create_team(request):
    if request.method == 'POST':
        team_form = TeamForm(request.POST or None,)

        if team_form.is_valid():
            team = team_form.save(commit=False)
            # Takes id of current user and saves them as captain
            team.captain = Player.objects.get(account=request.user.id)
            team.save()
            # This creates a new Membership for all the players selected from the form
            for player in team_form.cleaned_data['players'].all():
                Membership.objects.create(team_id=team.id, player_id=player.id)

            messages.success(request, 'Your team was successfully created!')
            return redirect('Team/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        team_form = TeamForm
    return render(request, 'tournee/team_creation.html', {
        'team_form': team_form,
    })


class TournamentUpdateView(generic.UpdateView):
    model = Tournament
    fields = ['teams', 'winners']
    template_name_suffix = "_edit"
    pk_url_kwarg = 'tournament_pk'
    context_object_name = 'tournament'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SeedUpdateView(generic.UpdateView):
    model = Seed
    fields = ['seed']
    template_name = "tournee/tournament_seeder.html"
    pk_url_kwarg = 'tournament_pk'
    context_object_name = 'seed'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def edit_seed(request, tournament):
    seed_form = SeedForm(request.POST or None)
    if seed_form.is_valid():
        # This means the tournament doesn't save until we've determined the captain
        seed = seed_form.save(commit=False)
        seed.save()
        # This part is more complex as it takes the many-to-many dropdown input and saves it as a new Seed record
        messages.success(request, 'Your seed was successfully created!')
        return redirect('Tournament/')
    else:
        messages.error(request, 'Please correct the error below.')
    return render(request, 'tournee/seed_edit.html', {
        'seed_form': seed_form,
    })
