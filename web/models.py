from django.db import models
from django.contrib.auth.models import User

class Novel(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_novels')
    by = models.CharField(max_length=200, default='RingoNovel')
    link = models.URLField(default='/')
    genre = models.CharField(max_length=50, default='khác')
    description = models.TextField(default='Tác giả nhỏ yếu bất lực, không thể viết tắttắt')
    chapters = models.IntegerField(default=0)
    co_authors = models.ManyToManyField(User, related_name='co_authored_novels', blank=True)
    cover_image = models.URLField(default='https://antimatter.vn/wp-content/uploads/2022/11/hinh-anh-anime-nu.jpg')
    like_count = models.IntegerField(default=0) #Số lượt thích
    followers = models.ManyToManyField(User, related_name='followed_novels', blank=True) #Người theo dõi
    create_at = models.DateTimeField(auto_now_add=True) #Ngày thêm vào
    status = models.CharField(max_length=50, default='ongoing')


    def __str__(self):
        return self.title

    @property
    def get_follow_count(self):
        return self.followers.count()

class Chapter(models.Model):
    novel = models.ForeignKey('Novel', on_delete=models.CASCADE)
    intChapter = models.IntegerField()
    title = models.CharField(max_length=200)
    content = models.TextField()
    read_count = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['intChapter']

    def __str__(self):
        return self.title

class Comment(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.URLField(default='https://antimatter.vn/wp-content/uploads/2022/11/hinh-anh-anime-nu.jpg')

    def __str__(self):
        return self.user.username
class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dark_mode = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Views_Novel(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='views_novel')
    views = models.IntegerField(default=0) #Lượt xem

    @classmethod
    def get_or_create(cls, novel):
        instance, created = cls.objects.get_or_create(novel=novel)
        return instance

    def __str__(self):
        return self.novel.title

