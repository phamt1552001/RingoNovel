from ..models import Novel, Chapter, Comment, Views_Novel
from ..novelRequest import MeTruyenChu
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db.models import Sum, Count, F, Value
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from datetime import timedelta



class NovelView:
    @staticmethod
    def index(request):
        novels = Novel.objects.all()
        limit = 12
        recent_time = now() - timedelta(days=30)

        novels = Novel.objects.annotate(
            follow_count=Count('followers'),
            total_views=Coalesce(Sum('views_novel__views'), Value(0)),  # Tránh None
            hot_score=F('follow_count') + F('total_views') + F('like_count')
    )


        novels_news = novels.order_by('-id')[:limit]
        top_novels = novels.order_by('-total_views')[:limit]
        hot_novels = novels.filter(create_at__gte=recent_time).order_by('-hot_score')[:limit]
        top_like_novels = Novel.objects.order_by('-like_count')[:limit]
        top_follow_novels = Novel.objects.annotate(follow_count=Count('followers')).order_by('-follow_count')[:limit]
        context = {
            "novels_news": novels_news,
            "top_novels": top_novels,
            "top_like_novels": top_like_novels,
            "top_follow_novels": top_follow_novels,
            "hot_novels": hot_novels,
        }
        return render(request, 'index.html', context)

    @staticmethod
    def detail(request, novel_id):
        novel = get_object_or_404(Novel, id=novel_id)
        chapters = Chapter.objects.filter(novel=novel).order_by('-intChapter')
        comments = Comment.objects.filter(novel=novel).order_by('-id')
        views_novel = Views_Novel.get_or_create(novel=novel)
        
        # _list = []
        # for value in chapters:
        #     _list.append(value.title)
            
        # newNovel = MeTruyenChu(novel.link)
        # __list = newNovel.getNovelChapter(_list)
        

        # for value in __list:
        #     Chapter.objects.create(
        #         novel = novel,
        #         intChapter = value[2],  # Tăng số chương
        #         title = value[0],
        #         content = value[1],
                
                
        #     )
        
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
    def create_novel_other(request):
        context = {}
        if request.method == 'POST':
            urlMeTruyenChu = request.POST.get('urlMeTruyenChu')
            if urlMeTruyenChu:
                novel = MeTruyenChu(urlMeTruyenChu)
                novel.getNovelDetail()
                try:
                    Novel.objects.create(
                    title = novel.title,
                    author = request.user,
                    by = 'MeTruyenChu',
                    link = urlMeTruyenChu,
                    genre = novel.genre,
                    description = novel.description,
                    cover_image = novel.img,
                    status = novel.status,
                )
                except Exception as e:
                    context['error'] = f"An error occurred: {str(e)}"
                
        
        return render(request,'create_novel_other.html',context)
    
    
    @staticmethod
    @login_required
    def list_chapters(request, novel_id):
        novel = get_object_or_404(Novel, id=novel_id, author=request.user)
        chapters = Chapter.objects.filter(novel=novel).order_by('-id')
        return render(request, 'list_chapter.html', {'novel': novel, 'chapters': chapters})
