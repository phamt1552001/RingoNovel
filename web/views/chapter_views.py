from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Novel, Chapter, Views_Novel
from ..forms import ChapterForm



class ChapterView:
    @staticmethod
    def read(request, novel_id, chapter_id):
        chapter = get_object_or_404(Chapter, id=chapter_id, novel_id=novel_id)
        chapter.read_count += 1
        chapter.save()

        views_novel, created = Views_Novel.objects.get_or_create(novel=chapter.novel)
        views_novel.views += 1
        views_novel.save()

        novel = chapter.novel
        return render(request, 'read_chapter.html', {'chapter': chapter, 'novel': novel})

    @staticmethod
    @login_required
    def add(request, novel_id):
        novel = get_object_or_404(Novel, id=novel_id, author=request.user)
        if request.method == 'POST':
            form = ChapterForm(request.POST)
            if form.is_valid():
                chapter = form.save(commit=False)
                chapter.novel = novel
                chapter.save()
                return redirect('novel_detail', novel_id=novel.id)
        else:
            form = ChapterForm()
        return render(request, 'add_chapter.html', {'form': form, 'novel': novel})
    
    @staticmethod
    @login_required
    def edit(request, chapter_id):
        chapter = get_object_or_404(Chapter, id=chapter_id)
        if request.method == 'POST':
            form = ChapterForm(request.POST, instance=chapter)
            if form.is_valid():
                form.save()
                return redirect('novel_detail', novel_id=chapter.novel.id)
        else:
            form = ChapterForm(instance=chapter)
        return render(request, 'edit_chapter.html', {'form': form, 'chapter': chapter})
