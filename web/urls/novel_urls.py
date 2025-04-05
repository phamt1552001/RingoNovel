from django.urls import path
from ..views import NovelView

urlpatterns = [
    path('', NovelView.index, name='index'),
    path('novel/<int:novel_id>/', NovelView.detail, name='novel_detail'),
    path('novel/<int:novel_id>/add_comment/', NovelView.add_comment, name='add_comment'),
    path('novel/create_novel_other/', NovelView.create_novel_other, name='create_novel_other'),
    path('find_novel/', NovelView.search, name='find_novel'),
    path('list_chapter/<int:novel_id>/', NovelView.list_chapters, name='list_chapter'),
]
