from django.contrib import admin
from .models import Novel, Chapter, Comment, Profile, Views_Novel

# Đăng ký các model với admin site
admin.site.register(Novel)
admin.site.register(Chapter)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Views_Novel)


