from datetime import datetime
from django.utils import timezone
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from cinema.models import Film
from cinema.serializers import FilmSerializer, FilmArchiveSerializer, FilmCalendarSerializer
from cinema.utils import ensure_film_omdb_up_to_date


class FilmArchiveApiView(APIView):
    """
    API view for handling film-related requests.
    """

    permission_classes: list = []
    authentication_classes: list = []

    def get(self, request: Request) -> Response:
        films = Film.objects.filter(omdb_json__isnull=False)

        # Parse the date string into a proper format
        for film in films:
            released_str = film.omdb_json.get("Released", "")
            try:
                film.omdb_json["Released"] = datetime.strptime(released_str, "%d %b %Y").date()
            except ValueError:
                film.omdb_json["Released"] = None

        # Filter films to only include those with a Released date in the past
        films = [film for film in films if
                 film.omdb_json.get("Released") and film.omdb_json["Released"] <= datetime.now().date()]

        # Sort the films by the parsed date
        films = sorted(films, key=lambda x: x.omdb_json.get("Released") or datetime.max.date(), reverse=True)

        paginator = PageNumberPagination()
        paginator.page_size = 6
        result_page = paginator.paginate_queryset(films, request)
        serializer = FilmArchiveSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class FilmDetailApiView(APIView):
    """
    API view for retrieving a single film by slug.
    """

    permission_classes: list = []
    authentication_classes: list = []

    def get(self, request: Request, slug: str) -> Response:
        film = get_object_or_404(Film, slug=slug)
        ensure_film_omdb_up_to_date(film)
        serializer = FilmSerializer(film)
        return Response(serializer.data, status=200)


class NowPlayingApiView(APIView):
    """
    API view for retrieving up to two 'now playing' films.
    """

    permission_classes: list = []
    authentication_classes: list = []

    def get(self, request: Request) -> Response:
        now = timezone.now()
        films = Film.objects.filter(
            bookings__booking_start_date__lte=now, bookings__booking_end_date__gte=now
        ).order_by("bookings__booking_start_date")[:2]
        serializer = FilmSerializer(films, many=True)
        return Response(serializer.data, status=200)


class ComingSoonApiView(APIView):
    """
    API view for retrieving up to two 'coming soon' films.
    """

    permission_classes: list = []
    authentication_classes: list = []

    def get(self, request: Request) -> Response:
        now = timezone.now()
        films = Film.objects.filter(
            bookings__booking_start_date__gt=now, bookings__confirmed=True
        ).order_by("bookings__booking_start_date")[:3]
        serializer = FilmSerializer(films, many=True)
        return Response(serializer.data, status=200)


class ComingSoonCalendarApiView(APIView):
    """
    API view for retrieving 'coming soon' films with a calendar format.
    """

    permission_classes: list = []
    authentication_classes: list = []

    def get(self, request: Request) -> Response:
        films = Film.objects.all()
        serializer = FilmCalendarSerializer(films, many=True)
        return Response(serializer.data, status=200)
