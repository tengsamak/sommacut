from django.urls import path
from . import views
app_name='products'
urlpatterns = [
    path('',views.index,name='index'),
    #path('category_products/',views.category_products),
    path('addcomment/<int:id>',views.addcomment,name='addcomment'),
   
]