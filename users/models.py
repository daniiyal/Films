import uuid

from django.db import models
from django.contrib.auth.models import User
from catalog.models import Film, Genre, Keyword


# Create your models here.


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid1, unique=True,
                          primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    genres = models.ManyToManyField(Genre, blank=True)
    keyword = models.ManyToManyField(Keyword, blank=True)

    def __str__(self):
        return self.user.username


class Watchlist(models.Model):
    class Meta:
        unique_together = (('film', 'user'),)

    id = models.UUIDField(default=uuid.uuid1, unique=True,
                          primary_key=True, editable=False)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'film']


class RatingStar(models.Model):
    value = models.SmallIntegerField(default=0)

    def __str__(self):
        return f"{self.value}"

    class Meta:
        ordering = ["-value"]


class Rating(models.Model):
    id = models.UUIDField(default=uuid.uuid1, unique=True,
                          primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.film} - {self.star}"

