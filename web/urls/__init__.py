from django.urls import path, include

urlpatterns = [
    path('', include('web.urls.novel_urls')),
    path('chapter/', include('web.urls.chapter_urls')),
    path('user/', include('web.urls.user_urls')),
    path('misc/', include('web.urls.misc_urls')),
    path('auth/', include('web.urls.auth_urls')),
    path('api/', include('web.urls.api_urls')),
]
