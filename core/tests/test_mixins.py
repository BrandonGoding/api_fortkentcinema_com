from django.test import TestCase
from django.db import IntegrityError
from cinema.models import Film  # Assuming Film model uses SlugModelMixin


class SlugModelMixinTestCase(TestCase):

    def test_slug_is_unique(self):
        # Create the first Film instance and save it
        film1 = Film.objects.create(
            title="Elio",
            imdb_id="1",
            youtube_id="1"
        )

        # Check that the slug is automatically generated and is unique
        self.assertIsNotNone(film1.slug)
        self.assertEqual(film1.slug, "elio")  # Assuming generate_slug uses the title

        # Now, we test the case of trying to save two films with the same slug
        # which should raise an IntegrityError due to the uniqueness constraint on the slug
        with self.assertRaises(IntegrityError):
            Film.objects.create(
                title="Elio",
                imdb_id="2",
                youtube_id="2"
            )
