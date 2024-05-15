from django.shortcuts import render
from category.models import Category
from store.models import *

# Create your views here.
def home(request):
    # Get all available courses
    courses = Course.objects.filter(is_available=True)
    
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Query the Order model to get the courses purchased by the user
        user_orders = Order.objects.filter(user=request.user)
        purchased_courses = [order.course for order in user_orders]
    else:
        purchased_courses = []  # If the user is not authenticated, initialize an empty list
        
    categories = Category.objects.all()
    
    context = {
        'courses': courses,
        'categories': categories,
        'purchased_courses': purchased_courses  # Pass purchased courses to the template
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request, 'contact.html')        

   