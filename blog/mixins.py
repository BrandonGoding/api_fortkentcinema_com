from django.db import models


class SlugModelMixin(models.Model):
    """
    Mixin to add slug functionality to models.
    Automatically generates a slug from the name field.
    """
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    class Meta:
        abstract = True

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = self.generate_slug()
    #     super().save(*args, **kwargs)
    #
    # def generate_slug(self):
    #     return models.slugify(self.name)
