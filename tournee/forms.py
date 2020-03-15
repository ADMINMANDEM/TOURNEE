from django import forms
from django.contrib.auth.models import User
from tournee.models import *


# This file is for defining what the forms use
class UserForm(forms.ModelForm):

    # This is so we can force the user input an email
    email = forms.CharField(max_length=75, required=True)

    class Meta:
        model = User
        fields = ('email', )


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('name', 'nationality', 'bio', 'teams')


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


class TournamentForm(forms.ModelForm):

    class Meta:
        model = Tournament
        fields = ('tournament_name', 'tournament_prize', 'winners', 'requirements', 'rules', 'time_and_date', 'teams')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["time_and_date"].widget = DateTimeInput()
        self.fields["time_and_date"].input_formats = ["%Y-%m-%dT%H:%M"]


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team

        fields = ('team_name', )

    def __init__(self, *args, **kwargs):

        # call the parent init
        super(TeamForm, self).__init__(*args, **kwargs)

        # change the widget to use checkboxes
        self.fields['players'] = forms.ModelMultipleChoiceField(
            queryset=Player.objects.all(),
            required=False,
            widget=forms.CheckboxSelectMultiple)


class SeedForm(forms.ModelForm):
    class Meta:
        model = Seed
        fields = ('team', 'seed')

    def __init__(self, *args, **kwargs):
        tournament = kwargs.pop('tournament')
        super(SeedForm, self).__init__(*args, **kwargs)
        self.fields['tournament'] = tournament
