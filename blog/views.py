from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework import status

# Create your views here.
class BlogPostListAPIView(APIView):
    """
    API view to retrieve a list of blog posts.
    """
    authentication_classes = []
    permission_classes = []
    
    def get(self, request, format=None):
        """
        Handle GET requests to retrieve a list of blog posts.
        """
        blog_posts = BlogPost.objects.all()
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data, status=200)

class BlogPostDetailAPIView(APIView):
    """
    API view to retrieve a single blog post.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, slug, format=None):
        try:
            blog_post = BlogPost.objects.get(slug=slug)
        except BlogPost.DoesNotExist:
            return Response({'detail': 'Blog post not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the previous and next posts
        prev_post = BlogPost.objects.filter(post_date__lt=blog_post.post_date).order_by('-post_date').first()
        next_post = BlogPost.objects.filter(post_date__gt=blog_post.post_date).order_by('post_date').first()

        serializer = BlogPostSerializer(blog_post)
        data = serializer.data
        data['prev_post'] = prev_post.slug if prev_post else None
        data['next_post'] = next_post.slug if next_post else None
        return Response(data, status=200)


