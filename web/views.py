from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Novel, Chapter, Comment, Profile, Views_Novel
from .forms import NovelForm, ChapterForm

class NovelView:
    @staticmethod
    def index(request):
        novels = Novel.objects.all()
        novels_news = novels.order_by('-id')[:12]
        top_novels = Novel.objects.annotate(view_count=Sum('views_novel__views')).order_by('-view_count')[:12]
        context = {
            "novels_news": novels_news,
            "top_novels": top_novels
        }
        return render(request, 'index.html', context)

    @staticmethod
    def detail(request, novel_id):
        novel = get_object_or_404(Novel, id=novel_id)
        chapters = Chapter.objects.filter(novel=novel).order_by('-intChapter')
        comments = Comment.objects.filter(novel=novel).order_by('-id')
        views_novel = Views_Novel.get_or_create(novel=novel)
        context = {
            "novel": novel,
            "chapters": chapters,
            "comments": comments,
            "views": views_novel,
        }
        return render(request, 'novel_detail.html', context)

    @staticmethod
    @login_required
    def add_comment(request, novel_id):
        if request.method == 'POST':
            novel = Novel.objects.get(id=novel_id)
            content = request.POST.get('content')
            Comment.objects.create(novel=novel, user=request.user, content=content)
            return redirect('novel_detail', novel_id=novel.id)

    @staticmethod
    def search(request):
        query = request.GET.get('query', '')
        chapters = request.GET.get('chapters', '')
        status = request.GET.get('status', '')
        genre = request.GET.get('genre', '')

        novels = Novel.objects.all()

        if query:
            novels = novels.filter(title__icontains=query)
        if chapters:
            if chapters == 'under_50':
                novels = novels.filter(chapters__lt(50))
            elif chapters == 'over_50':
                novels = novels.filter(chapters__gte(50))
            elif chapters == 'over_100':
                novels = novels.filter(chapters__gte(100))
            elif chapters == 'over_200':
                novels = novels.filter(chapters__gte(200))
            elif chapters == 'over_500':
                novels = novels.filter(chapters__gte(500))
        if status:
            novels = novels.filter(status=status)
        if genre:
            novels = novels.filter(genre=genre)

        paginator = Paginator(novels, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'results': page_obj,
            'query': query,
            'chapters': chapters,
            'status': status,
            'genre': genre
        }
        return render(request, 'find_novel.html', context)
    
    @staticmethod
    @login_required
    def list_chapters(request, novel_id):
        novel = get_object_or_404(Novel, id=novel_id, author=request.user)
        chapters = Chapter.objects.filter(novel=novel).order_by('-id')
        return render(request, 'list_chapter.html', {'novel': novel, 'chapters': chapters})

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

class UserView:
    @staticmethod
    def profile(request):
        return render(request, 'registration/profile.html')

    @staticmethod
    def settings(request):
        return render(request, 'settings.html')

    @staticmethod
    @login_required
    def author_area(request):
        novels = Novel.objects.filter(author=request.user).annotate(total_chapters=Count('chapter'))
        return render(request, 'author_area.html', {'novels': novels})

    @staticmethod
    @login_required
    def create_novel(request):
        if request.method == 'POST':
            form = NovelForm(request.POST)
            if form.is_valid():
                novel = form.save(commit=False)
                novel.author = request.user
                novel.save()
                return redirect('author_area')
        else:
            form = NovelForm()
        return render(request, 'create_novel.html', {'form': form})

    @staticmethod
    @login_required
    def edit_novel(request, novel_id):
        novel = get_object_or_404(Novel, id=novel_id, author=request.user)
        if request.method == 'POST':
            form = NovelForm(request.POST, instance=novel)
            if form.is_valid():
                form.save()
                return redirect('author_area')
        else:
            form = NovelForm(instance=novel)
        return render(request, 'edit_novel.html', {'form': form})

    @staticmethod
    @login_required
    def like_novel(request, novel_id):
        if request.method == 'POST':
            novel = get_object_or_404(Novel, id=novel_id)
            novel.like_count += 1
            novel.save()
            return JsonResponse({'like_count': novel.like_count})
        return JsonResponse({'error': 'Invalid request'}, status=400)

    @staticmethod
    @login_required
    def follow_novel(request, novel_id):
        novel = get_object_or_404(Novel, id=novel_id)
        if request.user in novel.followers.all():
            novel.followers.remove(request.user)
            followed = False
        else:
            novel.followers.add(request.user)
            followed = True
        return JsonResponse({'follow_count': novel.follow_count, 'followed': followed})

class MiscView:
    @staticmethod
    def check_errors(request):
        errors = []
        if not Novel.objects.exists():
            errors.append("No novels found in the database.")
        context = {
            "errors": errors
        }
        return render(request, 'check_errors.html', context)

    @staticmethod
    def donate(request):
        return render(request, 'donate.html')
