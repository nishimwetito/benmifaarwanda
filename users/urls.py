from django.urls import path
# from .views import register_view, login_view, logout_view, dashboard_view, profile_view,edit_profile,all_profiles,profile_detail,create_booking
from . import views

urlpatterns = [
   path('register/', views.register_view, name='register'),
   path('login/', views.login_view, name='login'),
   path('logout/', views.logout_view, name='logout'),
   path('dashboard/', views.user_dashboard, name='dashboard'),
   path('profile/', views.profile_view, name='profile'),
   path('profile/edit/',views. edit_profile, name='edit_profile'),
   path('profiles/', views.all_profiles, name='all_profiles'),
   path('profile/<str:username>/',views.profile_detail, name='profile_detail'),
   path('create/', views.create_booking, name='create_booking'),
   path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
   path('booking/create/', views.create_booking, name='create_booking'),
   path('booking/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),
   path('admin/booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
   path('admin/users/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),
   path('admin/booking/<int:booking_id>/delete/', views.delete_booking, name='delete_booking'),
]
