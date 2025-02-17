"""
URL configuration for NovelWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from web.views import NovelView, ChapterView, UserView, MiscView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', NovelView.index, name='index'),
    path('novel/<int:novel_id>/', NovelView.detail, name='novel_detail'),
    path('novel/<int:novel_id>/comment/', NovelView.add_comment, name='add_comment'),
    path('novel/<int:novel_id>/chapter/<int:chapter_id>/', ChapterView.read, name='read_chapter'),
    path('novel/<int:novel_id>/chapter/add/', ChapterView.add, name='add_chapter'),
    path('profile/', UserView.profile, name='profile'),
    path('settings/', UserView.settings, name='settings'),
    path('author_area/', UserView.author_area, name='author_area'),
    path('novel/create/', UserView.create_novel, name='create_novel'),
    path('novel/<int:novel_id>/edit/', UserView.edit_novel, name='edit_novel'),
    path('novel/<int:novel_id>/like/', UserView.like_novel, name='like_novel'),
    path('novel/<int:novel_id>/follow/', UserView.follow_novel, name='follow_novel'),
    path('check_errors/', MiscView.check_errors, name='check_errors'),
    path('donate/', MiscView.donate, name='donate'),
    path('search/', NovelView.search, name='search_novels'),
    path('find/', NovelView.find, name='find_novel'),
]
