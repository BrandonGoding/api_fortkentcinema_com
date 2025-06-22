from django.db import migrations
from django.utils.text import slugify


def slugify_blog(apps, schema_editor):

    BlogAuthor = apps.get_model("blog", "BlogAuthor")
    for author in BlogAuthor.objects.all():
        if not author.slug:
            BlogAuthor.objects.filter(pk=author.pk).update(
                slug=slugify(f"{author.first_name} {author.last_name}")
            )


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0008_auto_20250619_0205"),
    ]

    operations = [
        migrations.RunPython(slugify_blog, migrations.RunPython.noop),
    ]
