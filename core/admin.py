from django.contrib import admin
from .models import GalleryItem, Video, PDFGuide, Slide, ProfessionalSupportService, SiteSettings

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'description', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'show_on_homepage', 'homepage_order', 'instructor', 'duration', 'created_at')
    list_filter = ('category', 'show_on_homepage')
    list_editable = ('show_on_homepage', 'homepage_order')
    search_fields = ('title', 'description', 'instructor')

@admin.register(PDFGuide)
class PDFGuideAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'pages', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description', 'author')

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'presenter', 'slides_count', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description', 'presenter')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ProfessionalSupportService)
class ProfessionalSupportServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_on_homepage', 'homepage_order', 'tag_label', 'order', 'created_at')
    list_filter = ('show_on_homepage',)
    list_editable = ('show_on_homepage', 'homepage_order')
    search_fields = ('title', 'description', 'tag_label')
    ordering = ('homepage_order', 'order', '-created_at')
