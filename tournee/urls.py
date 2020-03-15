from django.urls import path, reverse
from . import views
from django.conf.urls import url


# These are the more specific urls for tournee
urlpatterns = [
    path('', views.index, name='index'),
    path('Tournament/', views.TournamentListView.as_view(), name='tournament-list'),
    # The /<int:pk> means we can view the individual tournament's information as it's own page
    path('Tournament/<int:pk>', views.TournamentDetailView.as_view(), name='tournament-detail'),
    path('Player/', views.PlayerListView.as_view(), name='player-list'),
    path('Player/<int:pk>', views.PlayerDetailView.as_view(), name='player-detail'),
    path('Team/', views.TeamListView.as_view(), name='team-list'),
    path('Team/<int:pk>', views.TeamDetailView.as_view(), name='team-detail'),
    path('Create_Tournament', views.create_tournament, name='create-tournament'),
    path('Create_Team', views.create_team, name='create-team'),
    path('Edit_Tournament/<int:pk>', views.TeamDetailView.as_view(), name='team-detail'),
    url(r'^Tournament/(?P<tournament_pk>\d+)/edit/$', views.TournamentUpdateView.as_view(), name='edit-tournament'),
    url(r'^Tournament/(?P<tournament_pk>\d+)/seed/$', views.SeedUpdateView.as_view(), name='edit-seed'),
    path('Edit_Seed', views.edit_seed, name='seed-form')
]
