from django.urls import path
from ..views import ChapterView

urlpatterns = [
    path('read/<int:novel_id>/<int:chapter_id>/', ChapterView.read, name='read_chapter'),
    path('add/<int:novel_id>/', ChapterView.add, name='add_chapter'),
    path('edit/<int:chapter_id>/', ChapterView.edit, name='edit_chapter'),
]
