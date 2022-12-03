from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    #path('category_products/',views.category_products),
    path('addtoshopcart/<int:id>',views.addtoshopcart,name='addtoshopcart'),
    path('deletefromcart/<int:id>',views.deletefromcart,name='deletefromcart'),
    path('orderproduct/',views.orderproduct,name='orderproduct'),
    # for pdf print weasyprint
    # path('admin/order/(?P<order_id>\d+)/pdf/$',views.admin_order_pdf,name='admin_order_pdf'),
    path('admin/order/<order_id>/pdf',views.admin_order_pdf,name='admin_order_pdf'),
    #for invoice pdf
    path('generate/pdf/<ordercode>/', views.generate_pdf, name='generate_pdf'),

]