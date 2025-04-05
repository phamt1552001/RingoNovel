from django.urls import path
from ..views import UserView

urlpatterns = [
    path('profile/', UserView.profile, name='profile'),
    path('settings/', UserView.settings, name='settings'),
    path('author_area/', UserView.author_area, name='author_area'),
    path('create_novel/', UserView.create_novel, name='create_novel'),
    path('edit_novel/<int:novel_id>/', UserView.edit_novel, name='edit_novel'),
    path('like_novel/<int:novel_id>/', UserView.like_novel, name='like_novel'),
    path('follow_novel/<int:novel_id>/', UserView.follow_novel, name='follow_novel'),
]
