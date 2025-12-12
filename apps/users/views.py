# apps/users/views.py — FINAL & 100% WORKING
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm


# ========================
# PUBLIC: Register (only if NOT logged in)
# ========================
def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect('landing')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


# ========================
# PUBLIC: Login (only if NOT logged in)
# ========================
def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect('landing')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.full_name or user.email}!")
            return redirect('landing')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'users/login.html')


# ========================
# Logout
# ========================
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('landing')


# ========================
# PROTECTED: Profile (only logged in)
# ========================
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # Handle avatar clear
            if 'avatar-clear' in request.POST:
                request.user.avatar.delete(save=False)
                request.user.avatar = None
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'users/profile.html', {
        'form': form,
        'user': request.user
    })