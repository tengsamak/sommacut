from django.urls import path, re_path
from . import views

urlpatterns = [
    path('',views.coupons,name='coupons'),
    path('couponapply/',views.coupon_apply,name='coupon_apply'),

]