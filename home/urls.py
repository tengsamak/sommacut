from django.urls import include, path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contactus/',views.contactus,name='contactus'),
    path('category/<int:id>/<slug:slug>/',views.category_products,name='category_products'),
]