from django.db import models


# My models
class Players(models.Model):
    name = models.CharField(db_column="Player's_Name", blank=True, null=True, max_length=32)
    team = models.CharField(db_column="Player's_Team", blank=True, null=True, max_length=32)
    username = models.CharField(db_column='Username', blank=True, null=True, max_length=32)
    password = models.CharField(db_column='Password', blank=True, null=True, max_length=16)
    email = models.EmailField(db_column='Email', blank=True, null=True)
    bio = models.CharField(db_column='Bio', blank=True, null=True, max_length=5000)
    teamid = models.CharField(db_column='TeamID', blank=True, null=True, max_length=8)


class Teams(models.Model):
    team_name = models.CharField(db_column='Team_Name', blank=True, null=True, max_length=32)
    playernames = models.TextField(db_column='Players', blank=True, null=True)
    captainid = models.ForeignKey(Players, on_delete=models.CASCADE)


Players.teamid = models.ForeignKey(Teams, on_delete=models.CASCADE)


class Tournaments(models.Model):
    tournament_name = models.CharField(db_column='Tournament_Name', blank=True, null=True, max_length=64)
    tournament_prize = models.CharField(db_column='Tournament_Prize', blank=True, null=True, max_length=5000)
    winners = models.CharField(db_column='Winners', blank=True, null=True, max_length=32)
    teamnames = models.TextField(db_column='Teams', blank=True, null=True)
    creatorid = models.ForeignKey(Players, on_delete=models.CASCADE)
    requirements = models.CharField(db_column='Requirements', blank=True, null=True, max_length=5000)
    rules = models.CharField(db_column='Rules', blank=True, null=True, max_length=5000)
    time_and_date = models.DateTimeField(auto_now_add=True, db_column='Time_and_Date', blank=True, null=True)
    scoreboard = models.TextField(db_column='Scoreboard', blank=True, null=True)
    in_progress = models.BooleanField(db_column='In_Progress', blank=True, null=True)
    tournamentline = models.IntegerField(db_column='TournamentLine', blank=True, null=True)


class TournamentResult(models.Model):
    team_id = models.ForeignKey(Teams, on_delete=models.CASCADE)
    result = models.SmallIntegerField(db_column='Result', blank=True, null=True)
    number_of_teams = models.SmallIntegerField(db_column='Number_of_Teams', blank=True, null=True)
    tournamentid = models.ForeignKey(Tournaments, on_delete=models.CASCADE)


class GameScores(models.Model):
    team_name = models.CharField(db_column='Team_Name', blank=True, null=True, max_length=32)
    team_1_score = models.SmallIntegerField(db_column='Team_1_Score', blank=True, null=True)
    team_2_score = models.SmallIntegerField(db_column='Team_2_Score', blank=True, null=True)
    matchid = models.ForeignKey(TournamentResult, on_delete=models.CASCADE)


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
