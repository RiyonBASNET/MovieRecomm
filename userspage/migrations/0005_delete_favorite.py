# Generated by Django 4.2.16 on 2024-11-07 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userspage', '0004_favorite'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]