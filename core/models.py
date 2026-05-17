from django.db import models

# Create your models here.

class GalleryItem(models.Model):
    CATEGORY_CHOICES = [
        ('Impact', 'Impact'),
        ('Training', 'Training'),
        ('Farming', 'Farming'),
        ('Wellness', 'Wellness'),
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=255, blank=True, help_text="e.g., Location or short detail")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category})"

    class Meta:
        ordering = ['-created_at']

class Course(models.Model):
    CATEGORY_CHOICES = [
        ('Wellness', 'Wellness'),
        ('Economy', 'Economy'),
        ('Farming', 'Farming'),
        ('Health', 'Health'),
        ('Community', 'Community'),
        ('Technical', 'Technical'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='course_thumbnails/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    duration = models.CharField(max_length=50, help_text="e.g. 30 mins", default="15 mins")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

class Video(models.Model):
    CATEGORY_CHOICES = [
        ('Training', 'Training'),
        ('Economy', 'Economy'),
        ('Farming', 'Farming'),
        ('Wellness', 'Wellness'),
    ]

    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    youtube_url = models.URLField(help_text="e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True, help_text="Optional: Upload a custom thumbnail. If blank, YouTube's thumbnail will be used.")
    instructor = models.CharField(max_length=100)
    duration = models.CharField(max_length=10, help_text="e.g., 15:30")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def youtube_id(self):
        """Extract YouTube video ID from various URL formats or raw ID"""
        import re
        # If already a valid ID
        if re.match(r'^[a-zA-Z0-9_-]{11}$', self.youtube_url):
            return self.youtube_url
            
        pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/|youtube\.com\/shorts\/|youtube\.com\/live\/)([a-zA-Z0-9_-]{11})'
        match = re.search(pattern, self.youtube_url)
        return match.group(1) if match else None

    @property
    def direct_youtube_url(self):
        video_id = self.youtube_id
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"
        return self.youtube_url

    @property
    def embed_url(self):
        """Convert YouTube watch URL to embed URL"""
        video_id = self.youtube_id
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return self.youtube_url

    @property
    def thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        video_id = self.youtube_id
        if video_id:
            return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        return ""

    class Meta:
        ordering = ['-created_at']

class PDFGuide(models.Model):
    CATEGORY_CHOICES = [
        ('Manual', 'Manual'),
        ('Tracker', 'Tracker'),
        ('Technical', 'Technical'),
        ('Guide', 'Guide'),
    ]

    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='pdfs')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    author = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='pdf_thumbnails/', help_text="Cover image for the PDF")
    pdf_file = models.FileField(upload_to='pdf_guides/')
    pages = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def file_size(self):
        """Returns the file size in MB"""
        try:
            size = self.pdf_file.size
            return f"{size / (1024 * 1024):.1f} MB"
        except:
            return "Unknown"

    class Meta:
        ordering = ['-created_at']

class Slide(models.Model):
    CATEGORY_CHOICES = [
        ('Workshop', 'Workshop'),
        ('Finance', 'Finance'),
        ('Farming', 'Farming'),
        ('Health', 'Health'),
        ('Community', 'Community'),
    ]

    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='slides')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    presenter = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='slide_thumbnails/', help_text="Cover image for the presentation")
    slide_file = models.FileField(upload_to='slides/', help_text="Upload PPTX or PDF slides")
    slides_count = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
