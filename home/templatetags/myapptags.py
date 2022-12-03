from django import template
from django.db.models import Sum
from django.urls import reverse

from ecommerce import settings


from products.models import Category

from order.models import ShopCart

register=template.Library()

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
def shopcartlist(request):
    # category = Category.objects.all()
    #current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=request.user)
    total = 0
    count_item=0 # for count items in Cart

    # for rs in shopcart:
    #     total += rs.product.price * rs.quantity
    #     count_item=count_item+1

    # this copy from youtube comment videos
    for rs in shopcart:
        count_item = count_item + 1
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity
    # return HttpResponse(str(total))
    # context = {'shopcart': shopcart,
    #            'category': category,
    #            'total': total,
    #            'count_item':count_item
    #            }
    return shopcart