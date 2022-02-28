import uuid

from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Film(models.Model):
    id = models.UUIDField(default=uuid.uuid1, unique=True,
                          primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000, null=True, blank=True)
    poster = models.ImageField(null=True, blank=True, default="default.png")
    genre = models.ManyToManyField('Genre')
    company = models.ManyToManyField('Company', blank=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    release_date = models.DateField(auto_now=False, auto_now_add=False, default=None)
    film_rating = models.FloatField(null=True)
    keyword = models.ManyToManyField('Keyword', blank=True)
    duration = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-film_rating']

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('user_id', flat=True)
        return queryset

    @property
    def calculate_rating(self):
        votes = self.rating_set.all()
        star_sum = 0
        for v in votes:
            star_sum += v.star.value
        self.film_rating = round(star_sum / votes.count(), 1)
        self.save()


class Role(models.Model):
    id = models.UUIDField(default=uuid.uuid1, unique=True,
                          primary_key=True, editable=False)
    role_name = models.CharField(max_length=30)

    def __str__(self):
        return self.role_name


class Genre(models.Model):
    id = models.UUIDField(default=uuid.uuid1, unique=True,
                          primary_key=True, editable=False)
    genre_name = models.CharField(max_length=30)
    genre_description = models.TextField(null=True)

    def __str__(self):
        return self.genre_name


class Company(models.Model):
    id = models.UUIDField(default=uuid.uuid1, unique=True,
                          primary_key=True, editable=False)
    company_name = models.CharField(max_length=50)

    def __str__(self):
        return self.company_name


class Country(models.Model):
    id = models.UUIDField(default=uuid.uuid1, unique=True,
                          primary_key=True, editable=False)
    country = models.CharField(max_length=30)

    def __str__(self):
        return self.country


class CastAndCrew(models.Model):
    id = models.UUIDField(default=uuid.uuid1, unique=True,
                          primary_key=True, editable=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    man = models.ForeignKey('People', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.man.name


class People(models.Model):
    id = models.UUIDField(default=uuid.uuid1, unique=True,
                          primary_key=True, editable=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False, unique=True)
    birthday = models.DateField(null=True, blank=True)
    deathday = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    VOTE_TYPE = (
        ('positive', 'Положительная'),
        ('negative', 'Отрицательная')
    )
    id = models.UUIDField(default=uuid.uuid1, unique=True,
                          primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'film']

    def __str__(self):
        return f'{self.value} - {self.film.title} - {self.user.username}'


class Keyword(models.Model):
    id = models.UUIDField(default=uuid.uuid1, unique=True,
                          primary_key=True, editable=False)
    keyword = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.keyword
