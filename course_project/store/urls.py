from django.urls import path
from .import views

urlpatterns = [
    path('allcourse/', views.allcourse , name ='allcourse'),
    path('store/', views.store , name = 'store'),
    path('category/<slug:category_slug>/', views.store, name='product_name'),
    path('category/<slug:category_slug>/<slug:course_slug>/', views.course_details, name='course_details'),
    path('cart/', views.cart , name ='cart'),
    path('category/<slug:category_slug>/<slug:course_slug>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout , name= 'checkout'),
    path('delete_from_cart/<int:course_id>', views.delete_from_cart, name='delete_from_cart'),
    path('payment_confirmation/<int:total_price>/', views.payment_confirmation, name='payment_confirmation'),
    path('course_tutorial/<int:course_id>', views.course_tutorial , name ='course_tutorial'),
    path('tutorial_details/<int:tutorial_id>', views.tutorial_details , name='tutorial_details'),
]
