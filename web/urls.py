from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import NovelView, ChapterView, UserView, MiscView, API_NovelViewSet

router = DefaultRouter()
router.register(r'apiNovels', API_NovelViewSet, basename='novel')


urlpatterns = [
    path('', NovelView.index, name='index'),
    
    #Novel
    path('novel/<int:novel_id>/', NovelView.detail, name='novel_detail'),
    path('novel/<int:novel_id>/add_comment/', NovelView.add_comment, name='add_comment'),
    path("novel/create_novel_other/", NovelView.create_novel_other, name="create_novel_other"),
    
    
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
    path('edit_chapter/<int:chapter_id>/', ChapterView.edit, name='edit_chapter'),
    path('list_chapter/<int:novel_id>/', NovelView.list_chapters, name='list_chapter'),
    path('check_errors/', MiscView.check_errors, name='check_errors'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('find_novel/', NovelView.search, name='find_novel'),
    
    #Rest_API
    path('',include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]