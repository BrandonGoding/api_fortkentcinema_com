from django.db import models
from django.utils import timezone

from core.mixins import SlugModelMixin


class Film(SlugModelMixin):
    title = models.CharField(max_length=100)
    imdb_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    youtube_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    omdb_json = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="bookings")
    booking_start_date = models.DateField()
    booking_end_date = models.DateField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"Booking for {self.film.title} from {self.booking_start_date}"
            f" to {self.booking_end_date}"
        )

    @property
    def is_active(self):
        return self.booking_start_date <= timezone.now().date() <= self.booking_end_date

    @property
    def is_confirmed(self):
        return self.confirmed

    class Meta:
        ordering = ["-booking_start_date"]
