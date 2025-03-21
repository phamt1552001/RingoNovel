from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User  # Add this import
from .models import Novel, Chapter, Comment, Profile, Views_Novel  # Replace with your actual model


class YourURLTestCase(TestCase):
    def test_homepage_url(self):
        response = self.client.get('/')  # Replace '/' with your URL path
        self.assertEqual(response.status_code, 200)

class NovelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.novel = Novel.objects.create(
            title="Test Novel",
            author=self.user,
            description="Test Description",
            like_count=10,
            chapters=5,
            status="ongoing",
            genre="fantasy"
        )
        self.novel.followers.add(self.user)  # Ensure followers field is populated

    def test_novel_creation(self):
        self.assertEqual(self.novel.title, "Test Novel")
        self.assertEqual(self.novel.author, self.user)
        self.assertEqual(self.novel.like_count, 10)
        self.assertEqual(self.novel.follow_count, 1)  # Test follow_count property

class ChapterTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="author", password="password")
        self.novel = Novel.objects.create(title="Test Novel", author=self.user)
        self.chapter = Chapter.objects.create(
            novel=self.novel,
            intChapter=1,
            title="Chapter 1",
            content="Test Content"
        )

    def test_chapter_creation(self):
        self.assertEqual(self.chapter.title, "Chapter 1")
        self.assertEqual(self.chapter.novel, self.novel)

class CommentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.novel = Novel.objects.create(title="Test Novel", author=self.user)
        self.comment = Comment.objects.create(
            novel=self.novel,
            user=self.user,
            content="Test Comment"
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, "Test Comment")
        self.assertEqual(self.comment.novel, self.novel)
        self.assertEqual(self.comment.user, self.user)

class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, "testuser")

class ViewsNovelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="author", password="password")
        self.novel = Novel.objects.create(
            title="Test Novel",
            author=self.user,
            description="Test Description",
            like_count=10,
            chapters=5,
            status="ongoing",
            genre="fantasy"
        )
        self.views_novel = Views_Novel.objects.create(novel=self.novel, views=100)

    def test_views_novel_creation(self):
        self.assertEqual(self.views_novel.novel.title, "Test Novel")
        self.assertEqual(self.views_novel.views, 100)

    def test_get_or_create_method(self):
        instance = Views_Novel.get_or_create(self.novel)
        self.assertEqual(instance.views, 100)
        self.assertEqual(instance.novel, self.novel)
