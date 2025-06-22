from django.db import migrations
from django.utils.text import slugify


def slugify_blog(apps, schema_editor):
    BlogCategory = apps.get_model("blog", "BlogCategory")
    for category in BlogCategory.objects.all():
        if not category.slug:
            BlogCategory.objects.filter(pk=category.pk).update(slug=slugify(category.name))


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0007_blogauthor_slug_blogpost_slug"),
    ]

    operations = [
        migrations.RunPython(slugify_blog, migrations.RunPython.noop),
    ]
