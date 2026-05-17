from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os


class Profile(models.Model):

    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    class MaritalStatus(models.TextChoices):
        SINGLE = 'single', 'Single'
        MARRIED = 'married', 'Married'
        DIVORCED = 'divorced', 'Divorced'
        WIDOWED = 'widowed', 'Widowed'

    # 🔗 RELATION
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    # 👤 PERSONAL INFO (Do NOT duplicate first_name, last_name)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    marital_status = models.CharField(max_length=10, choices=MaritalStatus.choices, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # 📍 LOCATION
    address = models.CharField(max_length=255, blank=True)

    # 🖼️ PROFILE IMAGE
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default='default.jpg',
        blank=True
    )

    # 🕒 SYSTEM FIELDS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Image optimization
        if self.profile_picture and self.profile_picture.name != 'default.jpg':
            img_path = self.profile_picture.path

            if os.path.exists(img_path):
                img = Image.open(img_path)

                if img.height > 300 or img.width > 300:
                    img.thumbnail((300, 300))
                    img.save(img_path)


class Booking(models.Model):
    """Booking model for user session bookings"""
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        COMPLETED = 'completed', 'Completed'
    
    SERVICE_CHOICES = [
        ('counseling', 'Family Counseling'),
        ('consulting', 'Business Consulting'),
        ('training', 'Group Training'),
    ]
    
    # User relationship
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    
    # Booking details
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    message = models.TextField(blank=True, help_text="Any specific questions or concerns")
    
    # Date & Time
    preferred_date = models.DateField()
    preferred_time = models.TimeField(null=True, blank=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_service_display()} ({self.get_status_display()})"
    
    def get_service_display(self):
        """Return readable service name"""
        return dict(self.SERVICE_CHOICES).get(self.service, self.service)
    
    def get_status_display(self):
        """Return readable status name"""
        return dict(self.Status.choices).get(self.status, self.status)