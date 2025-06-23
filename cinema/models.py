from datetime import datetime, time

from django.db import models
from django.utils import timezone

from core.mixins import SlugModelMixin


class Film(SlugModelMixin):
    title = models.CharField(max_length=100)
    imdb_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    youtube_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    omdb_json = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class Booking(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="bookings")
    booking_start_date = models.DateField()
    booking_end_date = models.DateField()
    confirmed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return (
            f"Booking for {self.film.title} from {self.booking_start_date}"
            f" to {self.booking_end_date}"
        )

    @property
    def is_active(self) -> bool:
        return self.booking_start_date <= timezone.now().date() <= self.booking_end_date

    @property
    def is_confirmed(self) -> bool:
        return self.confirmed

    class Meta:
        ordering = ["-booking_start_date"]


class PlayDate(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="play_dates")
    date = models.DateField()
    time = models.TimeField()

    def __str__(self) -> str:
        return f"{self.film.title} on {self.date} at {self.time}"

    @property
    def is_matinee(self) -> bool:
        if isinstance(self.time, str):
            show_time = datetime.strptime(self.time, "%H:%M:%S").time()
        else:
            show_time = self.time
        return show_time < time(16, 0)

    class Meta:
        unique_together = ("film", "date", "time")
        ordering = ["date", "time"]
