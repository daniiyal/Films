# Generated by Django 4.0.2 on 2022-02-18 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_genre_genre_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='genre_description',
            field=models.TextField(null=True),
        ),
    ]
