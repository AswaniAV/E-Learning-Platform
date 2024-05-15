from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login 
from store.models import *

def register(request):
    if request.method == 'POST':
        # Fetch form data
        firstname = request.POST.get('firstname', '').strip()
        lastname = request.POST.get('lastname', '').strip()
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirmpassword = request.POST.get('confirmpassword', '').strip()

        # Validation checks
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return redirect('register')  # Redirect to the 'register' URL name
        
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email already exists')
            return redirect('register')
        
        if password != confirmpassword:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()  # Save the changes
        
        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')  # Redirect to the 'login' URL name
    else:
        return render(request, 'register.html')  # Render the 'register.html' template


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # Log in the user
            return redirect('home')  # Redirect to the home page URL name
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')  # Redirect back to the 'login' URL name
    else:
        return render(request, 'login.html')  # Render the 'login.html' template


def logout(request):
    auth_logout(request)  # Log out the user
    messages.info(request, 'Logout successful.')
    return redirect('login')  # Redirect back to the 'login' URL name


def myprofile(request):
    course = Course.objects.filter(is_available=True)  # corrected query filter
    # check if the user is authenticated
    if request.user.is_authenticated:
        user_orders = Order.objects.filter(user=request.user)
        purchased_courses = [order.course for order in user_orders]
    else:
        purchased_courses = []  # if the user is not authenticated, initialize an empty list
    categories = Category.objects.all()

    context = {
        'categories': categories,
        'course': course,  # corrected variable name
        'purchased_courses': purchased_courses,
    } 
    return render(request, 'myprofile.html',context)
