from django import forms
from .models import Novel, Chapter

class NovelForm(forms.ModelForm):
    class Meta:
        model = Novel
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Tiêu đề', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Mô tả', 'class': 'form-control'}),
        }

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['intChapter', 'title', 'content']
        widgets = {
            'intChapter': forms.NumberInput(attrs={'placeholder': 'Số chương', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'placeholder': 'Tiêu đề chương', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'placeholder': 'Nội dung chương', 'class': 'form-control'}),
        }
