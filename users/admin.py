from django.contrib import admin
from .models import Profile, Watchlist, RatingStar, Rating
# Register your models here.

admin.site.register(Profile)
admin.site.register(Watchlist)
admin.site.register(Rating)
admin.site.register(RatingStar)