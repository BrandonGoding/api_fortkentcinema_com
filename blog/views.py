from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import BlogPost
from .serializers import BlogPostSerializer

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