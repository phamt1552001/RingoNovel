from django.urls import path
from ..views import MiscView

urlpatterns = [
    path('donate/', MiscView.donate, name='donate'),
    path('check_errors/', MiscView.check_errors, name='check_errors'),
]
