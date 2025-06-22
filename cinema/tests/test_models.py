from unittest import mock
from unittest.mock import Mock

from django.db import IntegrityError
from django.test import TestCase

from cinema.models import Film


class FilmModelTest(TestCase):
    def setUp(self) -> None:
        self.film = Film.objects.create(title="A Good Film", imdb_id="1234", youtube_id="5678")

    def test_imdb_id_is_unique(self) -> None:
        with self.assertRaises(IntegrityError):
            Film.objects.create(title="An OK Film", imdb_id="1234", youtube_id="9875")

    def test_youtube_id_is_unique(self) -> None:
        with self.assertRaises(IntegrityError):
            Film.objects.create(title="An OK Film", youtube_id="5678", imdb_id="9876")

    @mock.patch("core.mixins.slugify")
    def test_slugify_is_called_if_slug_is_none(self, mock_slugify: Mock) -> None:
        mock_slugify.return_value = "boom-slug"
        self.film.slug = None
        self.film.save()
        mock_slugify.assert_called_once_with("A Good Film")
