from django import forms
from .models import GalleryItem, Video, PDFGuide, Slide, Course

class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ['title', 'image', 'category', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter image title'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Kigali, 2024'}),
        }

class CourseForm(forms.ModelForm):
    # Optional initial resources
    youtube_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Optional: YouTube Link'}))
    pdf_file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    slide_file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Course
        fields = ['title', 'category', 'duration', 'description', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Title'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1 hour'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Learning objectives...', 'rows': 3}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'course', 'youtube_url', 'category', 'instructor', 'duration', 'description', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'youtube_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'instructor': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PDFGuideForm(forms.ModelForm):
    class Meta:
        model = PDFGuide
        fields = ['title', 'course', 'category', 'author', 'pages', 'description', 'thumbnail', 'pdf_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pdf_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class SlideForm(forms.ModelForm):
    class Meta:
        model = Slide
        fields = ['title', 'course', 'category', 'presenter', 'slides_count', 'description', 'thumbnail', 'slide_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'presenter': forms.TextInput(attrs={'class': 'form-control'}),
            'slides_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'slide_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
