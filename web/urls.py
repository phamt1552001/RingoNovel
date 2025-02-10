from django.urls import path
from django.contrib.auth import views as auth_views

from .views import NovelView, ChapterView, UserView, MiscView

urlpatterns = [
    path('', NovelView.index, name='index'),
    path('novel/<int:novel_id>/', NovelView.detail, name='novel_detail'),
    path('novel/<int:novel_id>/add_comment/', NovelView.add_comment, name='add_comment'),
    path('profile/', UserView.profile, name='profile'),
    path('read_chapter/<int:novel_id>/<int:chapter_id>/', ChapterView.read, name='read_chapter'),
    path('like_novel/<int:novel_id>/', UserView.like_novel, name='like_novel'),
    path('follow_novel/<int:novel_id>/', UserView.follow_novel, name='follow_novel'),
    path('settings/', UserView.settings, name='settings'),
    path('author_area/', UserView.author_area, name='author_area'),
    path('donate/', MiscView.donate, name='donate'),
    path('create_novel/', UserView.create_novel, name='create_novel'),
    path('edit_novel/<int:novel_id>/', UserView.edit_novel, name='edit_novel'),
    path('add_chapter/<int:novel_id>/', ChapterView.add, name='add_chapter'),
    path('check_errors/', MiscView.check_errors, name='check_errors'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('find_novel/', NovelView.search, name='find_novel'),
    path('search/', NovelView.search, name='search_novels'),
]