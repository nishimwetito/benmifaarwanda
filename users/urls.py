from django.urls import path
from . import views

urlpatterns = [
   path('register/', views.register_view, name='register'),
   path('login/', views.login_view, name='login'),
   path('logout/', views.logout_view, name='logout'),
   path('dashboard/', views.user_dashboard, name='dashboard'),
   path('profile/', views.profile_view, name='profile'),
   path('profile/edit/', views.edit_profile, name='edit_profile'),
   path('profiles/', views.all_profiles, name='all_profiles'),
   path('profile/<str:username>/', views.profile_detail, name='profile_detail'),
   path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
