from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from users.forms import RegisterForm
from .models import GalleryItem, Video, PDFGuide, Slide, Course
from .forms import GalleryItemForm, VideoForm, PDFGuideForm, SlideForm, CourseForm


# Create your views here.
def home_view(request):
    courses = Course.objects.all()[:3]
    return render(request, 'core/index.html', {
        'register_form': RegisterForm(),
        'courses': courses
    })


def gallery_view(request):
    if request.method == 'POST' and request.user.is_staff:
        form = GalleryItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Image uploaded successfully!')
            return redirect('gallery')
    else:
        form = GalleryItemForm()
        
    active_category = request.GET.get('category')
    if active_category:
        gallery_items_list = GalleryItem.objects.filter(category=active_category)
    else:
        gallery_items_list = GalleryItem.objects.all()
        
    paginator = Paginator(gallery_items_list, 6)
    page_number = request.GET.get('page')
    gallery_items = paginator.get_page(page_number)
        
    return render(request, 'core/gallery.html', {
        'gallery_items': gallery_items,
        'gallery_form': form,
        'active_category': active_category
    })


def edit_gallery_item(request, pk):
    if not request.user.is_staff:
        return redirect('gallery')
    
    item = get_object_or_404(GalleryItem, pk=pk)
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Image updated successfully!')
            return redirect('gallery')
    else:
        form = GalleryItemForm(instance=item)
    
    return render(request, 'core/edit_gallery.html', {'form': form, 'item': item})


def delete_gallery_item(request, pk):
    if not request.user.is_staff:
        return redirect('gallery')
    
    item = get_object_or_404(GalleryItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Image deleted successfully!')
        return redirect('gallery')
    
    return render(request, 'core/delete_gallery_confirm.html', {'item': item})


def courses_view(request):
    if request.method == 'POST' and request.user.is_staff:
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            
            # Create initial video if provided
            youtube_url = form.cleaned_data.get('youtube_url')
            if youtube_url:
                Video.objects.create(
                    title=f"{course.title} - Video",
                    course=course,
                    youtube_url=youtube_url,
                    category='Training',
                    description=course.description,
                    instructor="BE2SAHOBE Trainer",
                    duration=course.duration
                )
            
            # Create initial PDF if provided
            pdf_file = request.FILES.get('pdf_file')
            if pdf_file:
                PDFGuide.objects.create(
                    title=f"{course.title} - Guide",
                    course=course,
                    pdf_file=pdf_file,
                    category='Guide',
                    author="BE2SAHOBE Team",
                    description=course.description,
                    thumbnail=course.thumbnail # Reuse course thumbnail
                )
            
            # Create initial Slide if provided
            slide_file = request.FILES.get('slide_file')
            if slide_file:
                Slide.objects.create(
                    title=f"{course.title} - Slides",
                    course=course,
                    slide_file=slide_file,
                    category='Workshop',
                    presenter="BE2SAHOBE Team",
                    description=course.description,
                    thumbnail=course.thumbnail # Reuse course thumbnail
                )

            messages.success(request, 'Course curriculum and resources created successfully!')
            return redirect('courses')
    else:
        form = CourseForm()

    query = request.GET.get('q')
    if query:
        courses_list = Course.objects.filter(title__icontains=query) | Course.objects.filter(description__icontains=query)
    else:
        courses_list = Course.objects.all()

    paginator = Paginator(courses_list, 6)
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)

    return render(request, 'core/courses.html', {
        'courses': courses,
        'course_form': form,
        'query': query
    })


def edit_course_view(request, slug):
    if not request.user.is_staff:
        return redirect('courses')
    
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('courses')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'core/edit_course.html', {'form': form, 'course': course})


def delete_course_view(request, slug):
    if not request.user.is_staff:
        return redirect('courses')
    
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('courses')
    
    return render(request, 'core/delete_course_confirm.html', {'course': course})


def pdf_view(request):
    if request.method == 'POST' and request.user.is_staff:
        form = PDFGuideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'PDF Guide added successfully!')
            return redirect('pdf_list')
    else:
        form = PDFGuideForm()

    query = request.GET.get('q')
    if query:
        pdfs_list = PDFGuide.objects.filter(title__icontains=query) | PDFGuide.objects.filter(description__icontains=query)
    else:
        pdfs_list = PDFGuide.objects.all()

    paginator = Paginator(pdfs_list, 6)
    page_number = request.GET.get('page')
    pdfs = paginator.get_page(page_number)

    return render(request, 'core/pdf_list.html', {
        'pdfs': pdfs,
        'pdf_form': form,
        'query': query
    })


def edit_pdf_view(request, pk):
    if not request.user.is_staff:
        return redirect('pdf_list')
    
    pdf = get_object_or_404(PDFGuide, pk=pk)
    if request.method == 'POST':
        form = PDFGuideForm(request.POST, request.FILES, instance=pdf)
        if form.is_valid():
            form.save()
            messages.success(request, 'PDF Guide updated successfully!')
            return redirect('pdf_list')
    else:
        form = PDFGuideForm(instance=pdf)
    
    return render(request, 'core/edit_pdf.html', {'form': form, 'pdf': pdf})


def delete_pdf_view(request, pk):
    if not request.user.is_staff:
        return redirect('pdf_list')
    
    pdf = get_object_or_404(PDFGuide, pk=pk)
    if request.method == 'POST':
        pdf.delete()
        messages.success(request, 'PDF Guide deleted successfully!')
        return redirect('pdf_list')
    
    return render(request, 'core/delete_pdf_confirm.html', {'pdf': pdf})


def video_view(request):
    if request.method == 'POST' and request.user.is_staff:
        form = VideoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Video added successfully!')
            return redirect('video_list')
    else:
        form = VideoForm()

    query = request.GET.get('q')
    if query:
        videos_list = Video.objects.filter(title__icontains=query) | Video.objects.filter(description__icontains=query)
    else:
        videos_list = Video.objects.all()

    paginator = Paginator(videos_list, 6)
    page_number = request.GET.get('page')
    videos = paginator.get_page(page_number)

    return render(request, 'core/video_list.html', {
        'videos': videos,
        'video_form': form,
        'query': query
    })


def edit_video_view(request, pk):
    if not request.user.is_staff:
        return redirect('video_list')
    
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        form = VideoForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, 'Video updated successfully!')
            return redirect('video_list')
    else:
        form = VideoForm(instance=video)
    
    return render(request, 'core/edit_video.html', {'form': form, 'video': video})


def delete_video_view(request, pk):
    if not request.user.is_staff:
        return redirect('video_list')
    
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        video.delete()
        messages.success(request, 'Video deleted successfully!')
        return redirect('video_list')
    
    return render(request, 'core/delete_video_confirm.html', {'video': video})


def slides_view(request):
    if request.method == 'POST' and request.user.is_staff:
        form = SlideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Presentation added successfully!')
            return redirect('slides_list')
    else:
        form = SlideForm()

    query = request.GET.get('q')
    if query:
        slides_list = Slide.objects.filter(title__icontains=query) | Slide.objects.filter(description__icontains=query)
    else:
        slides_list = Slide.objects.all()

    paginator = Paginator(slides_list, 6)
    page_number = request.GET.get('page')
    slides = paginator.get_page(page_number)

    return render(request, 'core/slides_list.html', {
        'slides': slides,
        'slide_form': form,
        'query': query
    })


def edit_slide_view(request, pk):
    if not request.user.is_staff:
        return redirect('slides_list')
    
    slide = get_object_or_404(Slide, pk=pk)
    if request.method == 'POST':
        form = SlideForm(request.POST, request.FILES, instance=slide)
        if form.is_valid():
            form.save()
            messages.success(request, 'Presentation updated successfully!')
            return redirect('slides_list')
    else:
        form = SlideForm(instance=slide)
    
    return render(request, 'core/edit_slide.html', {'form': form, 'slide': slide})


def delete_slide_view(request, pk):
    if not request.user.is_staff:
        return redirect('slides_list')
    
    slide = get_object_or_404(Slide, pk=pk)
    if request.method == 'POST':
        slide.delete()
        messages.success(request, 'Presentation deleted successfully!')
        return redirect('slides_list')
    
    return render(request, 'core/delete_slide_confirm.html', {'slide': slide})


def professional_support_view(request):
    return render(request, 'core/professional_support.html')


def about_view(request):
    return render(request, 'core/about.html')


def partners_view(request):
    return render(request, 'core/partners.html')
