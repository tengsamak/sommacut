from django import template
from django.db.models import Sum
from django.urls import reverse
import decimal

from ecommerce import settings
from wishlist.models import wish_list
from datetime import datetime
from django.utils import timezone



from products.models import Category,Product,Variants

from order.models import ShopCart ,OrderProduct
from home.models import Paymentlist,Setting
import json

register=template.Library()

@register.simple_tag
def setting_info():
    info_setting=Setting.objects.get(pk=1)
    return info_setting.logo.url

@register.simple_tag
def todayrate():
    settingrate= Paymentlist.objects.get(setting=1)
    return settingrate.ratetoday

@register.simple_tag
def categorylist():
    return Category.objects.all()

@register.simple_tag
def stt(id,stop):
    id +=1
    if id == stop:
        pass
    return id



@register.simple_tag
def shopcartcount(userid):
    count = ShopCart.objects.filter(user_id=userid).count()
    return count

@register.simple_tag
def itemcount(ordercode):
    count = OrderProduct.objects.filter(order__code=ordercode).count()
    return count

@register.simple_tag
def shopcartgrandtotal(userid):
   # current_user = request.user # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=userid)
    grandtotal= 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            grandtotal += rs.product.price * rs.quantity
            #print("Total product:",total)
        else:
            if rs.variant is None:
                #total += rs.product.price * rs.quantity
                pass
            else:
                grandtotal += rs.variant.price * rs.quantity
    # No_VAT 0.00            
    vat10= grandtotal * decimal.Decimal(0.00) # convert float to decimal
    total=grandtotal
    grandtotal_ = total + vat10
    grandtotal='{:,.2f}'.format(grandtotal_)
    vat10='{:,.2f}'.format(vat10)
    total='{:,.2f}'.format(total)
    context={
        'grandtotal':grandtotal,
        'vat10':vat10,
        'total':total,
        
    }
    # print(context)
    # array = [{i: context[i]} for i in context]
    # jcontext=json.dumps(array)
    return context
    

#for wish list count templatetage
@register.simple_tag
def wishlistcount(userid):
    count=wish_list.objects.filter(user=userid).count()
    return count

@register.simple_tag
def shopcartlist(request):
    # category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user)
    return shopcart

@register.simple_tag
def countprobycate(cid):
    if cid == 63:
        products= Product.objects.filter(status=True)
    else:
        products=Product.objects.raw('SELECT * FROM products_product inner join products_category on (products_product.category_id=products_category.id) where products_product.status="True" AND products_category.parent_id= %s',[cid])
    countpro = 0
    for i in products:
        countpro+=1
        
    return countpro

from django.db.models import Count,Min,Max,Q 
@register.simple_tag
def leftsidebarpro():
    provenleftsidebar= Product.objects.values('category_id','category__title').annotate(countcate=Count('category_id')).filter(status=True)
    #print(provenleftsidebar)
    return provenleftsidebar 

@register.simple_tag
def max_price_leftside():
    #min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    return max_price
@register.simple_tag
def min_price_leftside():
    min_price = Product.objects.all().aggregate(Min('price'))
    #max_price = Product.objects.all().aggregate(Max('price'))
    return min_price

@register.simple_tag
def productcolorlist():
    varcolor=Variants.objects.values_list('color_id').distinct
    print(varcolor)
    return varcolor

#Math operator
@register.simple_tag()
def multiply(x, y, *args, **kwargs):
    # you would need to do any localization of the result here
    return round((decimal.Decimal(x) * decimal.Decimal(y)),2)
@register.simple_tag()
def devided(x, y, *args, **kwargs):
    # you would need to do any localization of the result here
    return decimal.Decimal(x/y)

@register.simple_tag()
def valueafterdiscount(x,y):
    #y is percentage or price<1
    # x is subtotal price
    return decimal.Decimal(x-(x*y/100))

@register.simple_tag()
def newgrandtotal(x):
    x=decimal.Decimal(x)
    #return round((x+(decimal.Decimal(x)*decimal.Decimal(0.1))),2)
    return round((x+x*decimal.Decimal(0.0)),2) # NO_VAT 0.00

@register.simple_tag()
def gapprice(mprice,sellprice):
    gapprice_=mprice - sellprice
    return f"{gapprice_:.2f}"

@register.filter
def percentage(value):
    return '{0:.0%}'.format(value) #format(value, "%")

from order.cart_session import Cartsession,Cartsession_no_var
@register.simple_tag()
def countsess(request):
    count_sess=Cartsession(request).__len__() + Cartsession_no_var(request).__len__()
    return count_sess

#for load sess header //call func with request
# from django.shortcuts import render
# from order.checkcart_sess import cart_header_sess
# @register.simple_tag
# def carthead_sess(request):
#     return cart_header_sess(request)

@register.simple_tag()
def categorybyvendor(vid):
    #category = Category.objects.all()
    products=Product.objects.filter(vendor_id=vid,status=True)
    setcategory=[]
    for i in products:
        setcategory.append(i.category.title)
    uniquecate=set(setcategory)
    return uniquecate
from products.models import Event_timer
@register.simple_tag()
def event_timer_tag_(pid):
    event_t=Event_timer.objects.filter(product_id=pid).count()
    print("eventtag:",event_t)
    if event_t > 0:
        event=Event_timer.objects.get(product_id=pid)
        if event.end_date <= timezone.now() :
            event.status="Expired"
            return event.status   
        else:
            return event     
    else:
        return None
    #return event

@register.simple_tag()
def event_timer_tag(pid):
    event_t=Event_timer.objects.filter(product_id=pid).count()
    print("eventtag:",event_t)
    if event_t > 0:
        event=Event_timer.objects.get(product_id=pid)
        event_check=event.discount_timer()
        if event_check == "Active" :
            
            return event   
        else:
            #event_check == "Expired" 
            return event_check + "Discount"    
        # else:
        #     return None
    else:
        return None
@register.simple_tag()    
def hot_deal():
    #select if have event_time countdown pro
    pid=8
    event_product=Event_timer.objects.filter(product=pid).count()
    if event_product>0:
        event=Event_timer.objects.get(product_id=pid)
        event_check=event.discount_timer()
        if event_check == "Active" :
            
            return event   
        else:
            #event_check == "Expired" 
            return timezone.now() 
    else:
        print(timezone.now())
        return timezone.now()
    
# best sale or top sale by products order the most
@register.simple_tag() 
def topsale():
    # Best Seller Produts
    count_order_p=OrderProduct.objects.values('product_id').annotate(count=Count('product_id')).order_by('-count')[:10]
    list_p_id=[] # for store product id 
    for i in count_order_p:
        # print("Pro:",i['product_id'])
        list_p_id.append(i['product_id'])
          
    #best sell product
    p_best_seller=Product.objects.filter(id__in=list_p_id)
    return p_best_seller