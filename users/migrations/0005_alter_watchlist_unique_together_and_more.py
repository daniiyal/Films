# Generated by Django 4.0.2 on 2022-02-19 11:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0009_alter_genre_genre_description'),
        ('users', '0004_profile_keyword'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='watchlist',
            unique_together={('user', 'film')},
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='rate',
        ),
    ]
