from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from . forms import RegisterForm


# Create your views here.
# REGISTER
def register_view(request):
    # if request.user.is_authenticated:
    #     return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save( commit= False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,'User created successfully!')
            login(request,user)
            return redirect('home')
            
        
    else:
        form = RegisterForm()

    context = {'form':form}

    return render (request, 'users/register.html',context)


def login_view(request):
#    if request.user.is_authenticated:
#        return redirect('dashboard')

   if request.method == 'POST':
       username = request.POST.get('username')
       password = request.POST.get('password')

       user = authenticate(request, username=username, password=password)

       if user is not None:
           login(request, user)
           messages.success(request,f'You are now logged in successfully as { request.user.username }')
           return redirect('home')
       else:
           messages.error(request, 'Invalid username or password')

   return render(request, 'users/login.html')


# LOGOUT
def logout_view(request):
   logout(request)
   messages.success(request,'Successfully logged out')
   return redirect('login')

# DASHBOARD (protected page)
def dashboard_view(request):
   if not request.user.is_authenticated:
       return redirect('login')




