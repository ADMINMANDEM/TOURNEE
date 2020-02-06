from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Tournaments/', views.TournamentListView.as_view(), name='tournaments-list'),
    path('Tournaments/<int:pk>', views.TournamentDetailView.as_view(), name='tournaments-detail'),
]
