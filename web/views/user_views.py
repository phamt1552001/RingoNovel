from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count

from ..models import Novel
from ..forms import NovelForm




class UserView:
    @staticmethod
    def profile(request):
        return render(request, 'registration/profile.html')

    @staticmethod
    def settings(request):
        """User settings view.
        FontEnd: web/templates/settings.html
            - Chế độ tối
            - 
        """
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
