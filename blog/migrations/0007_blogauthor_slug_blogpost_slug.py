# Generated by Django 5.2.3 on 2025-06-19 02:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0006_auto_20250619_0140"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogauthor",
            name="slug",
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="blogpost",
            name="slug",
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
