from django.db import migrations
from django.utils.text import slugify


def slugify_blog(apps, schema_editor):
    BlogPost = apps.get_model("blog", "BlogPost")
    for post in BlogPost.objects.all():
        if not post.slug:
            BlogPost.objects.filter(pk=post.pk).update(slug=slugify(post.subtitle))


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0009_auto_20250619_0209"),
    ]

    operations = [
        migrations.RunPython(slugify_blog, migrations.RunPython.noop),
    ]
