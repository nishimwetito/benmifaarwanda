from django.urls import path
from .views import (
    home_view, gallery_view, courses_view, 
    pdf_view, video_view, slides_view, 
    professional_support_view, about_view, partners_view,
    edit_gallery_item, delete_gallery_item,
    edit_video_view, delete_video_view,
    edit_pdf_view, delete_pdf_view,
    edit_slide_view, delete_slide_view,
    edit_course_view, delete_course_view
)
urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('partners/', partners_view, name='partners'),
    path('gallery/', gallery_view, name='gallery'),
    path('gallery/edit/<int:pk>/', edit_gallery_item, name='edit_gallery'),
    path('gallery/delete/<int:pk>/', delete_gallery_item, name='delete_gallery'),
    path('courses/', courses_view, name='courses'),
    path('courses/edit/<slug:slug>/', edit_course_view, name='edit_course'),
    path('courses/delete/<slug:slug>/', delete_course_view, name='delete_course'),
    path('courses/pdf/', pdf_view, name='pdf_list'),
    path('courses/pdf/edit/<int:pk>/', edit_pdf_view, name='edit_pdf'),
    path('courses/pdf/delete/<int:pk>/', delete_pdf_view, name='delete_pdf'),
    path('courses/video/', video_view, name='video_list'),
    path('courses/video/edit/<int:pk>/', edit_video_view, name='edit_video'),
    path('courses/video/delete/<int:pk>/', delete_video_view, name='delete_video'),
    path('courses/slides/', slides_view, name='slides_list'),
    path('courses/slides/edit/<int:pk>/', edit_slide_view, name='edit_slide'),
    path('courses/slides/delete/<int:pk>/', delete_slide_view, name='delete_slide'),
    path('support/', professional_support_view, name='professional_support'),
]