from django.shortcuts import get_object_or_404, render , redirect, HttpResponse
from store.models import *
from .models import *
from accounts.models import *
from category.models import Category
from django.contrib.auth.decorators import login_required
from urllib.parse import urlparse, parse_qs

def allcourse(request):
    course = Course.objects.all().filter(is_available= True)
    context = {
        'course' : course
    }
    return render(request,'allcourse.html',context)

def store(request,category_slug=None):
    courses = Course.objects.filter(is_available=True)
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        courses = courses.filter(category=category)

    context = {
        'courses': courses,
        'categories': categories,
    }
    return render(request, 'store.html', context)

def course_details(request,category_slug,course_slug):
    category = get_object_or_404(Category, slug=category_slug)
    course = get_object_or_404(Course, category=category, slug=course_slug)
    context ={
        'course' : course
    }
    return render(request,'course_details.html',context)

def cart(request):
    cart_course_ids = request.session.get('cart', []) 
    courses_in_cart = Course.objects.filter(id__in=cart_course_ids)
    total_price = sum(course.price for course in courses_in_cart)
    context = {
        'courses_in_cart': courses_in_cart,
        'total_price': total_price,
    }  
    return render(request, 'cart.html', context)    


def add_to_cart(request, category_slug, course_slug):
    category = get_object_or_404(Category, slug=category_slug)
    course = get_object_or_404(Course, slug=course_slug, category=category)
    if 'cart' not in request.session:
        request.session['cart'] = [] 
    request.session['cart'].append(course.id)
    request.session.modified = True
    return redirect('cart')

@login_required
def checkout(request):
    if request.method == 'POST':
        # Retrieve the course IDs from the session
        cart_course_ids = request.session.get('cart', [])
        # Check if the cart is empty
        if not cart_course_ids:
            # Redirect the user back to the cart page or any other appropriate page
            return redirect('cart')
        # Retrieve the courses in the cart
        courses_in_cart = Course.objects.filter(id__in=cart_course_ids)
        # Calculate total price and create orders
        total_price = 0  # Initialize total price
        for course_id in cart_course_ids:
            course = Course.objects.get(id=course_id)
            total_price += course.price  # Add course price to total price
            Order.objects.create(
                user=request.user,
                course=course,
                quantity=1,  # You may adjust this based on your requirements
                total_price=course.price  # Assuming each course's total price is its price
            )
        # Clear the cart after placing the order
        del request.session['cart']
        # Redirect the user to the payment confirmation page
        return redirect('payment_confirmation', total_price=total_price)
    return render(request, 'checkout.html')


def payment_confirmation(request, total_price):
    # Your view logic here
    return render(request, 'payment_confirmation.html', {'total_price': total_price})

def delete_from_cart(request,course_id):
    if 'cart' in request.session:
        cart_course_ids = request.session.get('cart')
        if course_id in cart_course_ids:
            cart_course_ids.remove(course_id)
            request.session['cart'] =cart_course_ids
            request.session.modified = True
    return redirect('cart')

def course_tutorial(request,course_id):
    try:
        course = Course.objects.get(pk=course_id)
        tutorials =Tutorial.objects.filter(course=course)
        total_modules = tutorials.count()
        context ={
            'course': course,
            'tutorials' : tutorials,
            'total_modules':total_modules,
        }
        return render(request, 'course_tutorial.html', context)
    except Course.DoesNotExist:
        return HttpResponse('course doesnot exist')

def tutorial_details(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, pk=tutorial_id)
    course = tutorial.course

    up_next_tutorials = Tutorial.objects.filter(course=course).exclude(pk=tutorial.pk)[:8]

    video_url = tutorial.video_url
    video_id = None
    if video_url:
        parsed_url = urlparse(video_url)
        if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
            video_id = parse_qs(parsed_url.query).get('v')
            if video_id:
                video_id = video_id[0]
        elif parsed_url.hostname in ['youtu.be']:
            video_id = parsed_url.path[1:]

    context = {
        'tutorial': tutorial,
        'up_next_tutorials': up_next_tutorials,
        'video_id': video_id,
    }
    return render(request, 'tutorial_details.html', context)

