#from django.urls import  path
# from . import views

# urlpatterns = [
#     path('',views.wishlist,name='wishlist'),
# ]

from django.views.generic import TemplateView

"""Urls for the wishlist app."""
from django.urls import path

from wishlist import views

app_name = 'wishlist'
urlpatterns = [
   
    path('add_wishlist',views.add_wishlist,name="add_wishlist"),
    #add_wishlist_session
    path('add_wishlist_session',views.add_wishlist_session,name="add_wishlist_session"),
    
    path('my_wishlist',views.my_wishlist,name='my_wishlist'),
    path('delete_from_wishlist',views.delete_from_wishlist,name='delete_from_wishlist'),
    #Wish List session view all products 
    path('my_wishlist_sess',views.view_wishlist_sess,name='view_wishlist_sess'),
    # Delete wish lis sess
    path('delete_from_wishlist_sess',views.delete_from_wishlist_sess,name='delete_from_wishlist_sess'),
]
