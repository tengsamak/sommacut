from django.urls import include, path
from . import views
app_name='user'
urlpatterns = [
    path('',views.index,name='userprofile'),
    path('update/',views.user_update,name='user_update'),
    path('password/',views.user_password,name='user_password'),
    path('orders/',views.user_orders,name='user_orders'),
    path('orderdetail/<int:id>',views.user_orderdetail,name='user_orderdetail'),
    path('orders_product/',views.user_order_product,name='user_order_product'),
    path('order_product_detail/<int:id>/<int:oid>',views.user_order_product_detail,name='user_order_product_detail'),
    path('comments/',views.user_comments,name='user_comments'),
    path('deletecomment/<int:id>',views.user_deletecomment,name='user_deletecomment'),
    #for url activate by signup with email verify 
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    #for forgetpassword reset link click via email
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
    #create subcribe for user
    path('subscribe', views.subscribe, name='subscribe'),
    #for newletter superuser sent to the subscriber
    path("newsletter", views.newsletter, name="newsletter"),
    #signup via phone number
    path("signupphone/", views.signupviaphone, name="signupviaphone"),

    path('indextest/',views.indextest,name='indextest'),
    
]