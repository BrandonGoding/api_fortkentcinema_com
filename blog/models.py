import uuid
from .mixins import SlugModelMixin
from django.db import models
from django.utils.text import slugify

# Create your models here.
class BlogAuthor(SlugModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class BlogCategory(SlugModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
        
class BlogPost(SlugModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    author = models.ForeignKey(BlogAuthor, on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    post_date = models.DateField()
    content = models.TextField()
    header_image = models.ImageField(upload_to="blog/images/", null=True, blank=True)
    
    class Meta:
        ordering = ['-post_date']
        
    def __str__(self):
        return self.subtitle