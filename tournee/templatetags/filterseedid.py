from django import template
from tournee.models import *

register = template.Library()


@register.simple_tag()
def seed_id(seed, team_id, tournament_id):
    return Seed.objects.get(team_id=seed.team.id, tournament_id=seed.tournament.id).id
