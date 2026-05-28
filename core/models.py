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

class Video(models.Model):
    CATEGORY_CHOICES = [
        ('Training', 'Training'),
        ('Economy', 'Economy'),
        ('Farming', 'Farming'),
        ('Wellness', 'Wellness'),
    ]

    title = models.CharField(max_length=200)
    youtube_url = models.URLField(help_text="e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True, help_text="Optional: Upload a custom thumbnail. If blank, YouTube's thumbnail will be used.")
    instructor = models.CharField(max_length=100)
    duration = models.CharField(max_length=10, help_text="e.g., 15:30")
    show_on_homepage = models.BooleanField(
        default=False,
        help_text="Display this video in the homepage learning section.",
    )
    homepage_order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers appear first on the homepage.",
    )
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


class ProfessionalSupportService(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(max_length=500, help_text="Service image URL")
    image_alt = models.CharField(max_length=200, blank=True)
    tag_label = models.CharField(max_length=80, blank=True, help_text="e.g. Data-Driven, Professional Branding")
    icon_class = models.CharField(
        max_length=80,
        default='bi-briefcase-fill',
        help_text="Bootstrap icon class, e.g. bi-diagram-3-fill",
    )
    email = models.EmailField(default='info@be2sahobe.rw')
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")
    show_on_homepage = models.BooleanField(
        default=False,
        help_text="Display this service on the landing page.",
    )
    homepage_order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers appear first on the homepage (among featured items).",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['homepage_order', 'order', '-created_at']


class SiteSettings(models.Model):
    """Singleton site-wide content and contact settings."""

    # Contact & social
    contact_address = models.CharField(max_length=255, default='Kigali, Rwanda')
    contact_phone = models.CharField(max_length=30, default='+250 788 487 127')
    contact_email = models.EmailField(default='hello@be2sahobe.com')
    whatsapp_number = models.CharField(
        max_length=20,
        default='250783558316',
        help_text='International format without +, e.g. 250783558316',
    )
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    footer_tagline = models.TextField(
        default='A digital ecosystem for holistic family living — integrating education, support, economic empowerment, and community across Africa.',
    )
    footer_copyright = models.CharField(
        max_length=255,
        default="© 2026 BE2SAHOBE LTD — We don't just teach, we help families IMPLEMENT change.",
    )

    donation_modal_title = models.CharField(max_length=120, default='Support our mission')
    donation_modal_subtitle = models.TextField(
        default='Your contribution helps families grow through holistic education and community support.',
    )
    momo_merchant_code = models.CharField(max_length=40, blank=True, default='123456')
    momo_account_name = models.CharField(max_length=120, blank=True, default='BE2SAHOBE LTD')
    bank_name = models.CharField(max_length=120, blank=True, default='Equity Bank Rwanda')
    bank_account_name = models.CharField(max_length=120, blank=True, default='BE2SAHOBE LIMITED')
    bank_account_number = models.CharField(max_length=120, blank=True, default='4000 1234 5678 9')

    donation_methods = models.JSONField(
        default=list,
        help_text='Donation methods list. Each item: {"title": "...", "icon": "bi-phone-fill", "rows": [{"label":"...","value":"..."}]}',
    )

    video_categories = models.JSONField(default=list, help_text='Video categories list')
    pdf_categories = models.JSONField(default=list, help_text='PDF guide categories list')
    slide_categories = models.JSONField(default=list, help_text='Slides categories list')
    gallery_categories = models.JSONField(default=list, help_text='Gallery categories list')

    # Home page — hero
    home_hero_badge = models.CharField(max_length=120, default='Digital Ecosystem for Families')
    home_hero_title_learn = models.CharField(max_length=40, default='Learn.')
    home_hero_title_grow = models.CharField(max_length=40, default='Grow.')
    home_hero_title_rest = models.CharField(max_length=80, default='Thrive. Together.')
    home_hero_subtitle = models.TextField(
        default='A transformative digital ecosystem empowering families through holistic living — integrating health, education, spiritual growth, economic empowerment, and sustainable community development.',
    )
    home_cta_primary_text = models.CharField(max_length=80, default='Explore Learning Programs')
    home_cta_primary_url = models.CharField(max_length=200, default='#learning')
    home_cta_secondary_text = models.CharField(max_length=80, default='Access Professional Support')
    home_cta_secondary_url = models.CharField(max_length=200, default='#services')
    home_stat_1_num = models.CharField(max_length=20, default='5')
    home_stat_1_label = models.CharField(max_length=80, default='Holistic Living Pillars')
    home_stat_2_num = models.CharField(max_length=20, default='1')
    home_stat_2_label = models.CharField(max_length=80, default='Integrated Family Ecosystem')
    home_stat_3_num = models.CharField(max_length=20, default='24/7')
    home_stat_3_label = models.CharField(max_length=80, default='Accessible Digital Support')
    home_card_title = models.CharField(max_length=120, default='Your Journey Starts Here')
    home_card_subtitle = models.CharField(max_length=120, default='Education → Support → Action')
    home_card_item_1 = models.CharField(max_length=200, default='Holistic Education & Digital Learning Resources')
    home_card_item_2 = models.CharField(max_length=200, default='Family Counseling, Mentorship & Christian Guidance')
    home_card_item_3 = models.CharField(max_length=200, default='Career Development & Economic Empowerment Programs')
    home_card_item_4 = models.CharField(max_length=200, default='Trusted Professional Consultancy & Community Support Services')
    home_card_button_text = models.CharField(max_length=80, default='Start Your Journey Today')

    # Home page — pillars section (editable list)
    home_pillars_label = models.CharField(max_length=60, default='Our Framework')
    home_pillars_title = models.CharField(max_length=120, default='The Five Foundations of Holistic Living')
    home_pillars = models.JSONField(
        default=list,
        help_text='List of pillars as JSON objects: [{"name": "...", "description": "...", "accent": "#RRGGBB"}]',
    )

    # About page
    about_hero_badge = models.CharField(max_length=80, default='Who We Are')
    about_hero_title = models.CharField(max_length=200, default='Empowering Families for')
    about_hero_title_highlight = models.CharField(max_length=120, default='Holistic Transformation')
    about_hero_subtitle = models.TextField(
        default='BE2SAHOBE LTD and MIFAA/NGoP work in synergy to provide Rwandan families with the tools, knowledge, and support needed to thrive in the modern world while staying rooted in community values.',
    )
    about_vision_title = models.CharField(max_length=80, default='Our Vision')
    about_vision_text = models.TextField(
        default='To be the leading digital ecosystem that empowers every Rwandan family to achieve holistic transformation and lasting prosperity, creating a future where every household is healthy, wealthy, and wise.',
    )
    about_mission_title = models.CharField(max_length=80, default='Our Mission')
    about_mission_text = models.TextField(
        default='To provide structured education, professional counseling, and practical economic tools that enable families to thrive across five key pillars: Body, Economy, Mind, Spirit, and Environment, through innovative digital platforms and community outreach.',
    )
    about_history_badge = models.CharField(max_length=80, default='Background & History')
    about_history_title = models.CharField(max_length=120, default='Our Journey')
    about_history_paragraph_1 = models.TextField(
        default='BE2SAHOBE LTD was established with a clear mandate: to bridge the gap between theoretical knowledge and practical action in family development. Recognizing that modern families face complex challenges, we developed a "Holistic Living" framework that addresses the body, mind, spirit, economy, and environment as an interconnected whole.',
    )
    about_history_paragraph_2 = models.TextField(
        default='In partnership with MIFAA/NGoP, our non-profit arm, we have expanded our reach to the most vulnerable communities, providing not just training, but the essential support systems like the IKIGEGA savings program and professional counseling.',
    )
    about_history_image = models.ImageField(upload_to='site/about/', blank=True, null=True)
    about_history_image_url = models.URLField(
        max_length=500,
        blank=True,
        default='https://images.pexels.com/photos/3184418/pexels-photo-3184418.jpeg?auto=compress&cs=tinysrgb&w=800',
        help_text='Used when no uploaded image is set',
    )
    about_history_card_title = models.CharField(max_length=120, default='Founded on Values')
    about_history_card_text = models.CharField(max_length=255, default='Blending tradition with digital innovation for family growth.')
    about_cta_title = models.CharField(max_length=120, default='Join Our Community')
    about_cta_text = models.TextField(
        default='Be part of a movement that is redefining family life in Rwanda. Start your journey toward holistic living today.',
    )
    about_cta_button_text = models.CharField(max_length=80, default='Get Started Now')

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def normalized_whatsapp(self):
        """Digits only, for wa.me links (e.g. 250783558316)."""
        raw = (self.whatsapp_number or '').strip()
        return ''.join(c for c in raw if c.isdigit())

    def whatsapp_display(self):
        """Human-readable number for templates."""
        digits = self.normalized_whatsapp()
        if not digits:
            return ''
        if digits.startswith('250') and len(digits) >= 12:
            return f"+{digits[:3]} {digits[3:5]} {digits[5:8]} {digits[8:]}"
        return f"+{digits}"

    def whatsapp_link(self, text=None):
        from urllib.parse import quote

        digits = self.normalized_whatsapp()
        if not digits:
            return ''
        url = f"https://wa.me/{digits}"
        if text:
            return f"{url}?text={quote(text)}"
        return url

    def about_history_image_src(self):
        if self.about_history_image:
            return self.about_history_image.url
        return self.about_history_image_url
