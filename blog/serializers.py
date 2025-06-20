from .models import BlogPost, BlogCategory, BlogAuthor
from rest_framework import serializers

class BlogPostAuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for BlogAuthor model.
    """
    class Meta:
        model = BlogAuthor
        fields = ['id', 'last_name', 'first_name', 'slug']
        read_only_fields = ['id']

class BlogCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for BlogCategory model.
    """
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id']

class BlogPostSerializer(serializers.ModelSerializer):
    """
    Serializer for BlogPost model.
    """
    author = BlogPostAuthorSerializer(read_only=True)
    category = BlogCategorySerializer(read_only=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'subtitle', 'author', 'category', 'post_date', 'content', 'slug']
        read_only_fields = ['id', 'post_date']
