from django.contrib import admin
from .models import Player, Team, Membership, Tournament, Seed


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1


class PlayerAdmin(admin.ModelAdmin):
    inlines = (MembershipInline,)


class SeedInline(admin.TabularInline):
    model = Seed
    extra = 1


class TournamentAdmin(admin.ModelAdmin):
    inlines = (SeedInline,)


class TeamAdmin(admin.ModelAdmin):
    inlines = (MembershipInline, SeedInline)


admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Tournament)
admin.site.register(Seed)
admin.site.register(Membership)
