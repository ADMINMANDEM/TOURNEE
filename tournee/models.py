from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# My models
# This defines the table player and gives the fields, their exceptions

class Player(models.Model):
    name = models.CharField(db_column="Player's_Name", null=True, max_length=32)
    nationality = models.CharField(db_column="Nationality", null=True, max_length=32)
    bio = models.CharField(db_column='Bio', blank=True, null=True, max_length=5000)
    # This OneToOneField is what gives a player an account that they login with. When the user creates an account, they
    # are immediately presented with the update profile page where they are made to enter their player details
    # (bio, teams, etc.)
    account = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    # The ManyToManyField is what links the teams the player is in to the player. The latter part means there is a
    # through table (or linking table) between the teams and players.
    teams = models.ManyToManyField('Team', through='Membership', through_fields=('player', 'team'), blank=True)

    # This means that when we call get_absolute_url, it returns an id which is used for a url that goes to a page of the
    # details of the player
    def get_absolute_url(self):
        return reverse('player-detail', args=[str(self.id)])

    # This means when I refer to Player instead of Player Object (1), I get the name of the player
    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(account=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.player.save()


class Team(models.Model):
    team_name = models.CharField(db_column='Team_Name', null=True, max_length=32)
    # the captain is an id from Player. This means we can click on the captain and see their page
    captain = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('team-detail', args=[str(self.id)])

    def __str__(self):
        return self.team_name


# This is the linking table between Player and Team
class Membership(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    # This is an extra field and means that whenever a player joins a team, the date at which they joined is recorded
    date_joined = models.DateField(auto_now_add=True, null=True)


class Tournament(models.Model):
    tournament_name = models.CharField(db_column='Tournament_Name', null=True, max_length=64)
    tournament_prize = models.CharField(db_column='Tournament_Prize', blank=True, null=True, max_length=5000)
    winners = models.CharField(db_column='Winners', null=True, max_length=32)
    creatorid = models.ForeignKey(Player, on_delete=models.CASCADE)
    requirements = models.CharField(db_column='Requirements', null=True, max_length=5000)
    rules = models.CharField(db_column='Rules', null=True, max_length=5000)
    time_and_date = models.DateTimeField(auto_now_add=False, db_column='Time_and_Date', null=True)
    teams = models.ManyToManyField(Team, through='Seed', blank=True, through_fields=('tournament', 'team'))

    def __str__(self):
        return self.tournament_name

    def get_absolute_url(self):
        return reverse('tournament-detail', args=[str(self.id)])


# Linking table for tournament and team
class Seed(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='participants')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    seed = models.IntegerField(db_column='Seed', null=True)

    def __str__(self):
        return str(self.seed)

    def get_absolute_url(self):
        return reverse('tournament-detail', args=[str(self.tournament.id)])


# BUILT IN DATABASE STUFF
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    last_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
