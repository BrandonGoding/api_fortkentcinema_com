# Generated by Django 5.2.3 on 2025-06-21 11:25
import json

from django.db import migrations
from django.utils.text import slugify


def load_films(apps, schema_editor):
    Film = apps.get_model("cinema", "Film")
    with open("cinema/fixtures/films.json") as file:
        films = json.load(file)

    for film_data in films:
        film = Film.objects.create(
            title=film_data["title"],
            youtube_id=film_data["youtube_id"],
            imdb_id=film_data["imdb_id"],
            slug=slugify(film_data["title"]),
        )
        for booking in film_data["bookings"]:
            film.bookings.create(
                booking_start_date=booking["booking_start_date"],
                booking_end_date=booking["booking_end_date"],
                confirmed=booking["confirmed"],
            )


class Migration(migrations.Migration):

    dependencies = [
        ("cinema", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_films),
    ]
