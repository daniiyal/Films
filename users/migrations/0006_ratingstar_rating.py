# Generated by Django 4.0.2 on 2022-02-24 16:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0009_alter_genre_genre_description'),
        ('users', '0005_alter_watchlist_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingStar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(default=0)),
            ],
            options={
                'ordering': ['-value'],
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False, unique=True)),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.film')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.ratingstar')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]