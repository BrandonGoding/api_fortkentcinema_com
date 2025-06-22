from django.contrib import admin

from blog.models import BlogAuthor, BlogCategory, BlogPost

# Register your models here.
admin.site.register(BlogAuthor)
admin.site.register(BlogCategory)
admin.site.register(BlogPost)
