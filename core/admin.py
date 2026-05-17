from django.contrib import admin
from .models import GalleryItem, Video, PDFGuide, Slide, Course

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1

class PDFGuideInline(admin.TabularInline):
    model = PDFGuide
    extra = 1

class SlideInline(admin.TabularInline):
    model = Slide
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'duration', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [VideoInline, PDFGuideInline, SlideInline]

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'description', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'category', 'instructor', 'duration', 'created_at')
    list_filter = ('category', 'course')
    search_fields = ('title', 'description', 'instructor')

@admin.register(PDFGuide)
class PDFGuideAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'category', 'author', 'pages', 'created_at')
    list_filter = ('category', 'course')
    search_fields = ('title', 'description', 'author')

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'category', 'presenter', 'slides_count', 'created_at')
    list_filter = ('category', 'course')
    search_fields = ('title', 'description', 'presenter')
