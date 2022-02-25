from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Film)
admin.site.register(Genre)
admin.site.register(Company)
admin.site.register(Keyword)
admin.site.register(Country)
admin.site.register(People)
admin.site.register(CastAndCrew)

