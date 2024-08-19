from django.urls import path
from . import views
app_name = 'home'
urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contactus/',views.contactus,name='contactus'),
    #path('category/<int:id>/<slug:slug>/',views.category_products,name='category_products'),
    path('searchcateid/<int:id>/<slug:slug>/',views.searchcateid,name='searchcateid'),
    #searchprocate search product by category_id
    path('searchprocate/<int:cid>/',views.searchprocate,name='searchprocate'),
    # product list filter by pricerange pricerangefilter
    path('pricerangefilter/',views.pricerangefilter,name='pricerangefilter'),
    # Sort by Ajax in Category template (no Vendor) with parent_id
    path('sortcate/',views.sortcate,name='sortcate'),
    # Sort by Ajax in Category template (no Vendor) with category_id
    path('sortprocate/',views.sortprocate,name='sortprocate'),
    
    
    path('searchcate/<int:id>/',views.searchcate,name='searchcate'),
    path('searchvendor/<int:vid>/<int:cid>/',views.searchvendor,name='searchvendor'),
    path('vendorlist/',views.vendorlist,name='vendorlist'),
    path('sortproven/',views.sortproven,name='sortproven'),
    path('provensearch_auto/<int:vid>/',views.provensearch_auto,name='provensearch_auto'),
    path('provensearchajax/',views.provensearchajax_test ,name='provensearchajax'),
    path('vendorsearch_auto/',views.vendorsearch_auto,name='vendorsearch_auto'),
    #termof service
    path('termofservices',views.termofservices,name='termofservices'),
    #privacypolicy
    path('privacypolicy',views.privacypolicy,name='privacypolicy'),
    #buyingguing buyingguide
    path('buyingguide',views.buyingguide,name='buyingguide'),
    #test product_listing_test
    path('productlisting',views.product_listing,name="productlisting"),
    # product tag name filter pro_filter_tag
    path('pro_filter_tag/<str:tagname>/',views.pro_filter_tag,name="pro_filter_tag"),
    # call expired_dis_timer function
    path('expired_dis_timer/',views.expired_dis_timer,name="expired_dis_timer"),
    
    
]