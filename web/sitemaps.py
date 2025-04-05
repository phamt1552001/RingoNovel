from django.contrib.sitemaps import Sitemap
from .models import Novel, Chapter

class NovelSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Novel.objects.all()

    def lastmod(self, obj):
        return obj.create_at  # hoặc obj.create_at nếu không có update

    def location(self, obj):
        return f"/novel/{obj.id}/"  # hoặc sử dụng reverse()

class ChapterSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Chapter.objects.all()

    def lastmod(self, obj):
        return obj.create_at

    def location(self, obj):
        return f"/read_chapter/{obj.novel.id}/{obj.id}/"
