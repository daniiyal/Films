# Generated by Django 4.0.2 on 2022-02-15 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_film_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='people',
            name='deathday',
            field=models.DateField(blank=True, null=True),
        ),
    ]