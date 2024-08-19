"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from home import views
from order import views as OrderViews # for កុំអោយErrors ជាមួយViews home or other views
from user import views as UserViews     # for កុំអោយErrors ជាមួយViews home or other views
from django.utils.translation import gettext_lazy as _   # for multilanguage

#for multilanguages
urlpatterns = [
    path('selectlanguage', views.selectlanguage, name='selectlanguage'),
   # path('selectcurrency', views.selectcurrency, name='selectcurrency'),
   # path('savelangcur', views.savelangcur, name='savelangcur'),
    path('i18n/', include('django.conf.urls.i18n')),
   # path('__debug__/', include(debug_toolbar.urls)), # for debug toolbar
]

# #translate link
urlpatterns += i18n_patterns(
    path('admin/',admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),  # ckeditor copy from weblink
    path('',include('home.urls'),name='index'),
    #path('about/',include('home.urls'),name='about'),
   # path('contactus/',include('home.urls'),name='contactus'),
    path('product/',include('products.urls')),
    path('order/',include('order.urls'),name='order'),
    path('user/',include('user.urls')),
    path('login/',UserViews.login__form,name='login_form'),
    path('logout/',UserViews.logout_func,name='logout_func'),
    #old signup link
    #path('signup/',UserViews.signup___form,name='signup_form'),
    # new signup verify by email
    path('signup/',UserViews.register,name='signup_form'),
    
    path('forgetpassword/',UserViews.password_reset_request,name='forgetpassword'),
    path('category/<int:id>/<slug:slug>',views.category_products,name='category_products'),
    path('searchbar/',views.searchbar,name='searchbar'), # for search normal
    path('search/',views.search,name='search'), # for search normal use SearchForm
    path('search_auto/',views.search_auto,name='search_auto'), # for search auto completed AJAX
    path('product/<int:id>/<slug:slug>',views.product_detail,name='product_detail'), # product detail link url
    #path('shopcart/',OrderViews.shopcart,name='shopcart'),
    path('faq/',UserViews.faq,name='faq'),
    
    path('ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),
    #test ajax selected pro
    path('selectedpro/',views.selectedpro, name='selectedpro'),
    
    path('vendors/',include('vendors.urls')),
    path('coupons/',include('coupons.urls')),
    path('wishlist/',include('wishlist.urls')), #for wish list url
    #install socialmedial login
    path('accounts/', include('allauth.urls')),
    # add for test allauth profile
    path('accounts/profile', include('allauth.urls')),

    prefix_default_language=False,
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from training
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns +=path('__debug__/', include(debug_toolbar.urls)), #for debug toolbar




# #orginal file
# urlpatterns = [
#     path('admin/',admin.site.urls),
#     path('ckeditor/', include('ckeditor_uploader.urls')),  # ckeditor copy from weblink
#     path('',include('home.urls')),
#     path('about/',include('home.urls'),name='about'),
#     path('contactus/',include('home.urls'),name='contactus'),
#     path('product/',include('products.urls')),
#     path('order/',include('order.urls')),
#     path('user/',include('user.urls')),
#     path('login/',UserViews.login___form,name='login_form'),
#     path('logout/',UserViews.logout_func,name='logout_func'),
#     path('signup/',UserViews.signup___form,name='signup_form'),
#     path('category/<int:id>/<slug:slug>',views.category_products,name='category_products'),
#     path('search/',views.search,name='search'), # for search normal
#     path('search_auto/',views.search_auto,name='search_auto'), # for search auto completed AJAX
#     path('product/<int:id>/<slug:slug>',views.product_detail,name='product_detail'), # product detail link url
#     path('shopcart/',OrderViews.shopcart,name='shopcart'),
#     path('faq/',UserViews.faq,name='faq'),
#     path('ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),
#     path('vendors/',include('vendors.urls')),
#     #install socialmedial login
#     path('accounts/', include('allauth.urls')),
#     # add for test allauth profile
#     path('accounts/profile', include('allauth.urls')),
# ]
#
# # from training
# if settings.DEBUG:
#     urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)