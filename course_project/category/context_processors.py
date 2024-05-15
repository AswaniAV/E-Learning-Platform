from category.models import Category 

def category_links(request):
    links = Category.objects.all() 
    return {
        'links': links, 
    }
