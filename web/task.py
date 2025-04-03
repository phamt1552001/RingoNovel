from background_task import background
from .models import Chapter,Novel
from .novelRequest import MeTruyenChu

@background(schedule=1)
def create_chapters_for_novel(novel_id, chapter_titles):
    novel = Novel.objects.get(id=novel_id)
    newNovel = MeTruyenChu(novel.link)
    chapters_data = newNovel.getNovelChapter(chapter_titles)
    
    new_chapters = []
    for value in chapters_data:
        new_chapters.append(Chapter(
            novel=novel,
            intChapter=value[2],
            title=value[0],
            content=value[1]
        ))

    Chapter.objects.bulk_create(new_chapters)
