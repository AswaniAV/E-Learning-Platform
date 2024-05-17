from django.contrib import admin
from .models import Course, Order, Tutorial  # Import both models from the same module

class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('course_name',)}
    list_display =('course_name','slug','course_img','category','desc','price','stock')

admin.site.register(Course, CourseAdmin)  # Register Course model with admin and apply custom admin options

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'total_price')  
    list_filter = ('user', 'order_date')
    search_fields = ('user__username', 'id')

admin.site.register(Order, OrderAdmin)  # Register Order model with admin and apply custom admin options

class TutorialAdmin(admin.ModelAdmin):
    list_display = ('title','course','video_url')

admin.site.register(Tutorial, TutorialAdmin)    