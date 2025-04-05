from django.shortcuts import render
from ..models import Novel

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
