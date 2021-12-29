from django.db import models
from django.contrib.auth.models import AbstractUser


class Team(models.Model):
    name = models.CharField(max_length=40)
    image_url = models.URLField(max_length=5000)

    def __str__(self):
        return self.name


class User(AbstractUser):
    image_url = models.URLField(max_length=5000, blank=True, null=True)
    levels = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    money = models.IntegerField(default=10000)
    team = models.ForeignKey(
        Team, on_delete=models.PROTECT, related_name="team", blank=True, null=True)


class Opponent(models.Model):
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, related_name='opponent', null=True)
    opposed_to = models.OneToOneField(
        User, on_delete=models.SET_NULL, related_name='opponent', null=True)


class General(models.Model):
    name = models.CharField(max_length=40)
    team = models.ForeignKey(
        Team, on_delete=models.PROTECT, related_name='generals', blank=True, null=True)
    commander = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="generals", blank=True, null=True)
    cap_image_url = models.URLField(max_length=5000)
    max_life = models.IntegerField(default=5)
    life = models.IntegerField(default=5)
    attack = models.IntegerField(default=80)
    defense = models.IntegerField(default=50)
    is_selected = models.BooleanField(default=False)
    leading_role = models.BooleanField(default=False)
    on_battle_k_u = models.IntegerField(default=0)
    killed_units = models.IntegerField(default=0)
    as_opponent = models.ForeignKey(Opponent, on_delete=models.SET_NULL,
                                    related_query_name='generals', related_name='generals', blank=True, null=True)

    def __str__(self):
        return self.name


class Soldier(models.Model):
    commander = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="soldiers", blank=True, null=True)
    helmet_image_url = models.URLField(max_length=5000)
    max_life = models.IntegerField(default=2)
    life = models.IntegerField(default=2)
    attack = models.IntegerField(default=70)
    defense = models.IntegerField(default=40)
    on_battle_k_u = models.IntegerField(default=0)
    killed_units = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='soldiers',
                             related_query_name='soldiers', blank=True, null=True)
    as_opponent = models.ForeignKey(Opponent, on_delete=models.SET_NULL,
                                    related_name='soldiers', related_query_name='soldiers', blank=True, null=True)


class Score(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, related_name='score', blank=True, null=True)
    user_score = models.IntegerField(default=0)
    opponent_score = models.IntegerField(default=0)
    opponent = models.OneToOneField(
        Opponent, on_delete=models.SET_NULL, related_name='score', blank=True, null=True)


class Product(models.Model):
    name = models.CharField(max_length=20)
    image_url = models.URLField(max_length=5000)
    price = models.IntegerField()
    category = models.CharField(max_length=20)
    power = models.IntegerField(default=5)

    def __str__(self):
        return self.name
