# Generated by Django 4.0.2 on 2022-02-14 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='release_date',
            field=models.DateField(default=None),
        ),
    ]