from django.urls import include, path
from . import views
app_name='vendors'
urlpatterns = [
    path('',views.vendorsapp,name='vendorsapp'),
    path('update/',views.vendor_update,name='vendor_update'),
    path('productlist/',views.vendorproductlist,name='vendor_product_list'),
    path('productdetail/<int:pid>/',views.vendorproductdetail,name='vendorproductdetail'),
    path('productorder/<int:pid>/',views.vendorproductorder,name='vendorproductorder'),
    path('productordercode/',views.vendorproductinvoice,name='vendorproductinvoice'),
    path('productstatistic/',views.vendorstatistic,name='vendorstatistic'),
    path('productstatisticlistorderbyid/<int:uid>/',views.vendorstatisticlistinvoicebyid,name='vendorstatisticlistinvoicebyid'),
    #addcomment_v for vendor
    path('addcomment_v/<int:vid>',views.addcomment_v,name='addcomment_v'),
    #add follower Ajax
    #path('add_follower/',views.add_follower,name='add_follower'),
    
]