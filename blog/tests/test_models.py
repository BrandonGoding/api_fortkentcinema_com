from django.test import TestCase

from blog.models import BlogAuthor, BlogCategory, BlogPost


class BlogPostTestCase(TestCase):
    def setUp(self):
        self.author = BlogAuthor.objects.create(last_name='last_name', first_name='first_name', slug='slug')
        self.category = BlogCategory.objects.create(name='title', slug='slug')
        self.post = BlogPost.objects.create(title='title', subtitle='subtitle', slug='slug', author=self.author, category=self.category, content='content', post_date="2025-01-01")

    def test_str(self):
        self.assertEqual(str(self.post), self.post.subtitle)

class BlogAuthorTestCase(TestCase):
    def setUp(self):
        self.author = BlogAuthor.objects.create(last_name='last_name', first_name='first_name', slug='slug')

    def test_str(self):
        self.assertEqual(str(self.author), f"{self.author.first_name} {self.author.last_name}")

class BlogCategoryTestCase(TestCase):
    def setUp(self):
        self.category = BlogCategory.objects.create(name='title', slug='slug')

    def test_str(self):
        self.assertEqual(str(self.category), f"{self.category.name}")