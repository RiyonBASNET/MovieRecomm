# Generated by Django 4.2.16 on 2024-09-23 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MovieInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movieTitle', models.CharField(max_length=100)),
                ('movieReleaseDate', models.CharField(max_length=100)),
                ('movieDescription', models.TextField()),
                ('image', models.CharField(max_length=255)),
                ('trailerUrl', models.CharField(max_length=255)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]