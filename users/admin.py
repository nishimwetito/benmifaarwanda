from django.contrib import admin
from .models import Profile, Booking

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'address', 'created_at']
    search_fields = ['user__username', 'first_name', 'phone_number']
    list_filter = ['phone_number', 'created_at']



@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'preferred_date', 'status')
    list_filter = ('status', 'service')
    search_fields = ('user__username',)