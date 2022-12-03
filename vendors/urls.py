from django.urls import include, path
from . import views

urlpatterns = [
    path('',views.vendorsapp,name='vendorsapp'),
    path('update/',views.vendor_update,name='vendor_update'),
    path('productlist/',views.vendorproductlist,name='vendor_product_list'),
    path('productdetail/<int:pid>/',views.vendorproductdetail,name='vendorproductdetail'),
    path('productorder/<int:pid>/',views.vendorproductorder,name='vendorproductorder'),
    path('productordercode/',views.vendorproductinvoice,name='vendorproductinvoice'),
    path('productstatistic/',views.vendorstatistic,name='vendorstatistic'),
    path('productstatisticlistorderbyid/<int:uid>/',views.vendorstatisticlistinvoicebyid,name='vendorstatisticlistinvoicebyid'),

]