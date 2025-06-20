import json
from django.db import migrations

def update_header_images(apps, schema_editor):
    BlogPost = apps.get_model('blog', 'BlogPost')
    with open('blog/fixtures/blog.json', 'r') as f:
        data = json.load(f)
    for entry in data:
        title = entry.get('title')
        header_image = entry.get('header_image')
        if title and header_image:
            try:
                post = BlogPost.objects.get(title=title)
                post.header_image = header_image
                post.save()
            except BlogPost.DoesNotExist:
                continue

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_blogpost_options_blogpost_header_image'),
    ]

    operations = [
        migrations.RunPython(update_header_images),
    ]