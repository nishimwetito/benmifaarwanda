from django.shortcuts import render,redirect,get_object_or_404, reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from . forms import RegisterForm
from .models import Profile,Booking


# Create your views here.
# REGISTER
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User created successfully!')
            login(request, user)
            return redirect(f"{reverse('dashboard')}?tab=profile")
    else:
        messages.error(request, 'Registration failed')
        form = RegisterForm()

    context = {'register_form': form}
    return render(request, 'index.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {user.username}')
            return redirect(f"{reverse('dashboard')}?tab=profile")
        else:
            messages.error(request, 'Invalid username or password')

    return redirect('home')


# LOGOUT
def logout_view(request):
   logout(request)
   messages.success(request,'Successfully logged out')
   return redirect('login')

# USER PROFILE

@login_required
def profile_view(request):
    """
    Redirect to the unified dashboard profile tab.
    """
    return redirect('/dashboard/?tab=profile')


@login_required
def edit_profile(request):
    """
    Handle profile editing via modal form
    """
    if request.method == 'POST':
        # Get the current user and profile
        user = request.user
        profile = user.profile
        
        # Update User model fields
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Check if username is taken (exclude current user)
        if User.objects.exclude(id=user.id).filter(username=username).exists():
            messages.error(request, 'This username is already taken.')
            return redirect('profile')
        
        # Update user fields
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        # Update Profile model fields
        profile.gender = request.POST.get('gender')
        profile.marital_status = request.POST.get('marital_status')
        profile.phone_number = request.POST.get('phone_number')
        
        date_of_birth = request.POST.get('date_of_birth')
        if date_of_birth:
            from datetime import datetime
            profile.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        
        profile.address = request.POST.get('address')
        
        # Handle profile picture upload
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('profile')
    
    return redirect('profile')




@login_required
def all_profiles(request):
    """
    Display all registered user profiles with search and filter
    """
    # Get all profiles
    profiles_list = Profile.objects.select_related('user').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        profiles_list = profiles_list.filter(
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(address__icontains=search_query)
        )
    
    # Filter by gender
    gender_filter = request.GET.get('gender', '')
    if gender_filter:
        profiles_list = profiles_list.filter(gender=gender_filter)
    
    # Pagination (12 profiles per page)
    paginator = Paginator(profiles_list, 12)
    page_number = request.GET.get('page')
    profiles = paginator.get_page(page_number)
    
    context = {
        'profiles': profiles,
        'total_members': Profile.objects.count(),
        'search_query': search_query,
        'gender_filter': gender_filter,
    }
    return render(request, 'users/all_profiles.html', context)


@login_required
def profile_detail(request, username):
    """
    Display detailed profile of a specific user
    """
    profile = get_object_or_404(Profile, user__username=username)
    
    context = {
        'viewed_profile': profile,
    }
    return render(request, 'users/profile_details.html', context)




# ============================================================
# USER VIEWS
# ============================================================

@login_required
def user_dashboard(request):
    """
    Unified Dashboard - Handles both regular users and staff.
    """
    active_tab = request.GET.get('tab', 'overview')
    user = request.user
    profile = user.profile
    
    # 1. User's Own Bookings
    user_bookings = Booking.objects.filter(user=user).order_by('-created_at')
    
    context = {
        'active_tab': active_tab,
        'profile': profile,
        'user_bookings': user_bookings,
        'total_user': user_bookings.count(),
        'pending_user': user_bookings.filter(status='pending').count(),
        'approved_user': user_bookings.filter(status='approved').count(),
    }
    
    # 2. Staff Specific Data
    if user.is_staff:
        # All Bookings with filters
        all_bookings = Booking.objects.all().order_by('-created_at')
        
        status_filter = request.GET.get('status', '')
        if status_filter:
            all_bookings = all_bookings.filter(status=status_filter)
            
        search_query = request.GET.get('search', '')
        if search_query:
            all_bookings = all_bookings.filter(
                Q(user__username__icontains=search_query) |
                Q(user__email__icontains=search_query)
            )
            
        # All Members with search/filter
        all_profiles_list = Profile.objects.select_related('user').all()
        member_search = request.GET.get('member_search', '')
        if member_search:
            all_profiles_list = all_profiles_list.filter(
                Q(user__username__icontains=member_search) |
                Q(user__first_name__icontains=member_search) |
                Q(user__last_name__icontains=member_search)
            )
            
        # Stats for Admin
        admin_stats = {
            'total': Booking.objects.count(),
            'pending': Booking.objects.filter(status='pending').count(),
            'approved': Booking.objects.filter(status='approved').count(),
            'total_members': Profile.objects.count(),
        }
        
        context.update({
            'all_bookings': all_bookings,
            'all_profiles': all_profiles_list,
            'admin_stats': admin_stats,
            'status_filter': status_filter,
            'search_query': search_query,
            'member_search': member_search,
        })
    
    return render(request, 'users/dashboard.html', context)


@login_required
def create_booking(request):
    """Create a new booking from modal form"""
    if request.method == 'POST':
        service = request.POST.get('service')
        message = request.POST.get('message')
        preferred_date = request.POST.get('preferred_date')
        preferred_time = request.POST.get('preferred_time')
        
        # Validation
        if not service or not preferred_date:
            messages.error(request, "Service and preferred date are required.")
            return redirect('dashboard')
        
        # Create booking
        Booking.objects.create(
            user=request.user,
            service=service,
            message=message or "",
            preferred_date=preferred_date,
            preferred_time=preferred_time or None,
            status=Booking.Status.PENDING
        )
        
        messages.success(request, "✅ Booking request sent successfully! We will contact you soon.")
        return redirect('dashboard')
    
    return redirect('dashboard')


# ============================================================
# ADMIN VIEWS (Staff Only)
# ============================================================

@staff_member_required
def admin_dashboard(request):
    """
    Redirect to the unified dashboard management tab.
    """
    return redirect('/dashboard/?tab=manage_bookings')


@staff_member_required
def booking_detail(request, booking_id):
    """View full booking details with user profile information"""
    booking = get_object_or_404(Booking, id=booking_id)
    profile = booking.user.profile
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_status':
            new_status = request.POST.get('status')
            if new_status in ['pending', 'approved', 'rejected', 'completed']:
                booking.status = new_status
                booking.save()
                messages.success(request, f"✅ Booking #{booking.id} status updated to {booking.get_status_display()}")
                return redirect('booking_detail', booking_id=booking.id)
        
        elif action == 'delete':
            booking.delete()
            messages.success(request, f"🗑️ Booking #{booking_id} has been deleted.")
            return redirect('admin_dashboard')
    
    context = {
        'booking': booking,
        'profile': profile,
    }
    return render(request, 'users/booking_detail.html', context)


@staff_member_required
def update_booking_status(request, booking_id, status):
    """Quick update booking status with confirmation"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    valid_statuses = ['approved', 'rejected', 'completed']
    if status not in valid_statuses:
        messages.error(request, "Invalid status update.")
        return redirect('admin_dashboard')
    
    booking.status = status
    booking.save()
    
    status_display = {
        'approved': 'Approved',
        'rejected': 'Rejected',
        'completed': 'Completed'
    }.get(status, status)
    
    messages.success(request, f"✅ Booking #{booking.id} has been {status_display}.")
    return redirect('admin_dashboard')


@staff_member_required
def delete_booking(request, booking_id):
    """Delete a booking with confirmation"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        booking_id_value = booking.id
        booking.delete()
        messages.success(request, f"🗑️ Booking #{booking_id_value} has been permanently deleted.")
        return redirect('admin_dashboard')
    
    # GET request - show confirmation page
    return render(request, 'users/confirm_delete.html', {'booking': booking})