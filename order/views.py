import decimal
import tempfile
from datetime import datetime


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse, reverse_lazy
"""
for the pdf export
"""
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
# from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

# Create your views here.
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views import View
#from django_simple_coupons.validations import validate_coupon,Coupon,CouponUser

from .models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from products.models import Product, Category, Variants

from user.models import UserProfile

from home.models import Setting , Paymentlist




#from django_simple_coupons.models import Coupon



from coupons.form import CouponApplyForm


def index(request):
    return HttpResponse('order page')

# test link*******
def addtoshopcart__t(request,id):
    return HttpResponse(str(id))

@login_required(login_url='/login') # Check login
def addtoshopcart(request,id): # from detail product
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product = Product.objects.get(pk=id)
    #print("####Product get PK with variant:",product.variant)
    if product.variant != 'None':    #mean that have Variants
        variantid = request.POST.get('variant_id')  # from variant add to cart
        print("****varinat form:", variantid)
        checkinvariant = ShopCart.objects.filter(variant_id=variantid,user_id=current_user.id)  # Check product in shopcart
        if checkinvariant:
            control = 1  # The product is in the cart with variant
        else:
            control = 0  # The product is not in the cart with variant"""
    else:   # mean NO Variant
        checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id)  # Check product in shopcart
        if checkinproduct:
            control = 1  # The product is in the cart with No variant
        else:
            control = 0  # The product is not in the cart with No variant"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart
                if product.variant == 'None': 
                    data = ShopCart.objects.get(product_id=id, user_id=current_user.id)

                else:
                    
                    #**************
                    #need to check varinats table because each variant price different or color or size
                    #*******************
                    #if colorid or sizeid or color&sizeid:
                    
                    #samak add code
                    
                    # end samak add code       
                    data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id) #have variant
              
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
               
                messages.success(request,"your the same existing product/variant add to shopcart")
            else:  # Inser to Shopcart
                data = ShopCart()
                # self add code
                if product.variant == 'None':
                #      data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                    data.product_id = id
                    messages.success(request,"New shopCart Product=None")
                else:
                    #data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)
                    
                    #samak add code
                    #getvar = request.POST.get('variant_id')

                    #end samak add code
                    data.product_id = id
                    #data.product_id = id
                    #print("print get var outsid:",int(getvar))
                    data.variant_id = variantid
                    #data.variant_id = getvar
                    messages.success(request,"New ShopCart Variants")
                            # end code
                #data = ShopCart()
                data.user_id = current_user.id
                #data.product_id = id
                #data.variant_id=form.cleaned_data['variantid']
                #data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
                
                messages.success(request,"New product/Variant added to shopcart")
        messages.success(request, "Product added to Shopcart by Form Control Product/Variant!")
        messages.warning(request, 'Click on ShopCart Icon for your oder..')
        #return JsonResponse(dataajax)
        return HttpResponseRedirect(url)
    #click from index by herf a tag HTML
    else:  # if there is no post 
            # mean click on icon Cart
        
        if control == 1:  # Update  shopcart
            #variant_id = request.GET['variantid']
            #print("###########variant click=",variant_id)
            if product.variant == 'None': 
                data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            else:
                data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)
                
            #data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()  #
            
        else:  # Inser to Shopcart
            data = ShopCart() # model ile bağlantı kur
            if product.variant == 'None':
                data.product_id = id
                
            else:
                data.product_id = id
                data.variant_id = variantid
                
            data.user_id = current_user.id    
            data.quantity = 1
            data.save() 
    #add more check variant for that products add by click in index or wishlist
           

        # messages.success(request, "Product added to Shopcart by from Home/index/search page!")
        # messages.warning(request,'Click on ShopCart Icon for your oder..')
        #return JsonResponse(dataajax)
        return HttpResponseRedirect(url)

# Add to Cart with No Variant by Ajax
@login_required(login_url='/login')
#from django.contrib import auth
def add_tocart_no_variant(request):
    # pid= request.POST.get('product')
    pid= request.POST['product']
    qty = request.POST['qty']
    #pid=request.GET['product']
    #qty = request.GET['qty']
    current_user = request.user
    print("pid and qty*************",pid,qty)
    #pvariant=request.GET['pvariant']
    #product=Product.objects.get(pk=pid)
    print("quantity:",qty)
    data={}
    checkcart=ShopCart.objects.filter(product_id=pid,user_id=current_user.id)
    print(checkcart)
    if (checkcart):
        if int(qty) > 1:
            print("already Product ID In Cart with quantity>1")
            getcart = ShopCart.objects.get(product_id=pid,user_id=current_user.id)
            getcart.quantity += int(qty)
        else:
            print("already Product ID In Cart with not quantity or equal 1")
            # add increase 1 by quantity
            getcart = ShopCart.objects.get(product_id=pid,user_id=current_user.id)
            getcart.quantity += 1
     
    else:
        if int(qty) > 1:
            getcart = ShopCart()
            getcart.product_id = pid
            getcart.user_id = current_user.id
            getcart.quantity += int(qty)
        else:        
            print("don't have id product with no varinat in Cart")
            getcart = ShopCart()
            getcart.product_id = pid
            getcart.user_id = current_user.id
            #getcart.variant_id = variant
            getcart.quantity = 1
    
    getcart.save()
    cartcount = ShopCart.objects.filter(user_id=current_user).count()
    #test add to cartlist
    shopcart = ShopCart.objects.filter(user=request.user).order_by('id')
    count = ShopCart.objects.filter(user=request.user).order_by('id').count()
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            if rs.variant is None:
                pass
            else:
                total += rs.variant.price * rs.quantity
    # return HttpResponse(str(total))
    #NO_VAT 0.00
    vat10= total * decimal.Decimal(0.00) # convert float to decimal
    grandtotal=total + vat10
    #coupon_apply_form = CouponApplyForm()
    contextajax = {'shopcart': shopcart,
               #'category': category,
               'total': total,
               'vat10': vat10,
               'grandtotal':grandtotal,
               #'coupon_apply_form':coupon_apply_form,
               'count':count,
               }
    #end test
    data={
			'status':True,
            'cartcount':cartcount,
            'rendered_table': render_to_string('cartlistajax.html', context=contextajax),
		}
    return JsonResponse(data)
    #return JsonResponse({'bool':True})
    #return JsonResponse()

# Add to Cart by Ajax with variant
@login_required(login_url='/login')
def add_tocart_with_variant(request):
    current_user = request.user
    #pid=request.POST['pid']
    pid=request.POST.get('pid')
    #varid=request.POST['varid']
    varid=request.POST.get('varid')
    #qty = request.POST['qty']
    qty = request.POST.get('qty')
    #for get request
    #pid=request.GET['pid']
    #varid=request.GET['varid']
    #qty = request.GET['qty']
    print("id,var,qty",pid,varid,qty)
    data={}
    #check product with productid and variantid
    check = ShopCart.objects.filter(product_id=pid,variant_id=varid,user_id=current_user.id)
    if check:
        # product id with variant have already in cart so just updat quantity
        print("Your product add to cart with variant already in cart")
        getcart = ShopCart.objects.get(product_id=pid,variant_id=varid,user_id=current_user.id)
        getcart.quantity += qty
    else:
        #product id and variant don't 
        print("Your product add to cart with variant New in cart")
        getcart = ShopCart()
        getcart.product_id = pid
        getcart.variant_id = varid
        getcart.quantity = qty
        getcart.user_id = current_user.id
        
    getcart.save()
    cartcount = ShopCart.objects.filter(user_id=current_user).count()
    #add test to cartlist by ajax
    shopcart = ShopCart.objects.filter(user=request.user).order_by('id')
    count = ShopCart.objects.filter(user=request.user).order_by('id').count()
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            if rs.variant is None:
                pass
            else:
                total += rs.variant.price * rs.quantity
    # return HttpResponse(str(total))
    #NO_VAT 0.00
    vat10= total * decimal.Decimal(0.00) # convert float to decimal
    grandtotal=total + vat10
    #coupon_apply_form = CouponApplyForm()
    contextajax = {'shopcart': shopcart,
               #'category': category,
               'total': total,
               'vat10': vat10,
               'grandtotal':grandtotal,
               #'coupon_apply_form':coupon_apply_form,
               'count':count,
               }
    #end add test
    
    data={'success':True,
          'cartcount':cartcount,
          'rendered_table': render_to_string('cartlistajax.html', context=contextajax),
          }
    print(data)
    return JsonResponse(data)
    


@login_required(login_url='/login')
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id).order_by('id')
    shopcartcount = ShopCart.objects.filter(user_id=current_user.id).order_by('id').count()
    #shopcart = ShopCart.objects.filter(user_id=current_user.id).order_by('id').values()
    total = 0


    # count_item=0 # for count items in Cart

    # for rs in shopcart:
    #     total += rs.product.price * rs.quantity
    #     count_item=count_item+1

    # this copy from youtube comment videos
    for rs in shopcart:

        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        # else:
        #     total += rs.variant.price * rs.quantity
            
        else:
            if rs.variant is None:
                #add product from wish list
                #total += rs.product.price * rs.quantity
                pass
            else:
                total += rs.variant.price * rs.quantity
    # return HttpResponse(str(total))
    # No_VAT 0.00
    vat10= total * decimal.Decimal(0.00) # convert float to decimal
    
    grandtotal=total  + vat10
    #'{:,.2f}'.format(num), Print number with commas as 1000 separators in
    #grandtotal='{:,}'.format(grandtotal_)
    # for 3 digit ex: '1000.50' to '1,000.50'
    grandtotal='{:,.2f}'.format(grandtotal)
    vat10 ='{:,.2f}'.format(vat10)
    total ='{:,.2f}'.format(total)
    # print("total and Grand:",total,grandtotal)


    #coupon_apply_form = CouponApplyForm()


    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'vat10': vat10,
               'grandtotal':grandtotal,
               #'coupon_apply_form':coupon_apply_form,
               'shopcartcount':shopcartcount,
               }
    return render(request, 'shopcart_products.html', context)

#shop cart list by Ajax For header content
@login_required(login_url='/login') 
def cartlistajax(request):
    data={}
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id).order_by('id')
    count = ShopCart.objects.filter(user_id=current_user.id).order_by('id').count()
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            if rs.variant is None:
                pass
            else:
                total += rs.variant.price * rs.quantity
    # return HttpResponse(str(total))
    # No_VAT 0.00
    vat10= total * decimal.Decimal(0.00) # convert float to decimal
    grandtotal=total + vat10
    # for 3 digit ex: '1000.50' to '1,000.50'
    grandtotal='{:,.2f}'.format(grandtotal)
    vat10 ='{:,.2f}'.format(vat10)
    total ='{:,.2f}'.format(total)
    #coupon_apply_form = CouponApplyForm()
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'vat10': vat10,
               'grandtotal':grandtotal,
               #'coupon_apply_form':coupon_apply_form,
               'count':count,
               }
    data = {'rendered_table': render_to_string('cartlistajax.html', context=context)}
        
    return JsonResponse(data)

@login_required(login_url='/login')  # Check login not ajax
def deletefromcart(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    # cartid=str(request.GET['wid'])
    ShopCart.objects.filter(id=id).delete()
    # cartcount=ShopCart.objects.filter(user=request.user).count()
    #data={'status'}
   
    # return JsonResponse({'status':1,'carttcount':cartcount})
    # messages.success(request, "Your item deleted form Shopcart.")
    #return HttpResponseRedirect("/shopcart")
    return HttpResponseRedirect(url)

# delete from cart list by Ajax
@login_required(login_url='/login') 
def delete_from_cartlist(request):
    data={}
    cart_id=str(request.POST['cartid'])
    #requestGET
    #cart_id=str(request.GET['cartid'])
    get_cartid=ShopCart.objects.get(pk=int(cart_id))
    get_cartid.delete()
    cartlistcount=ShopCart.objects.filter(user=request.user).count()
    print("you product was delete from Cart List Ajax")
    #add test
    shopcart = ShopCart.objects.filter(user=request.user).order_by('id')
    count = ShopCart.objects.filter(user=request.user).order_by('id').count()
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            if rs.variant is None:
                pass
            else:
                total += rs.variant.price * rs.quantity
    # return HttpResponse(str(total))
    # No_VAT 0.00
    vat10= total * decimal.Decimal(0.00) # convert float to decimal
    grandtotal=total + vat10
    #coupon_apply_form = CouponApplyForm()
    contextajax = {'shopcart': shopcart,
               #'category': category,
               'total': total,
               'vat10': vat10,
               'grandtotal':grandtotal,
               #'coupon_apply_form':coupon_apply_form,
               'count':count,
               }
    #end test
    context={
        'status':1,
        'cartlistcount':cartlistcount, 
        'rendered_table': render_to_string('cartlistajax.html', context=contextajax),   # for display at header
    }
    data=context
    #t=render_to_string('wish_list_del_response.html')
    return JsonResponse(data)

@login_required(login_url='/login') 
def delete_from_cartlist_1(request):
    #data={}
    cart_id=str(request.POST['cartid'])
    #requestGET
    #cart_id=str(request.GET['cartid'])
    get_cartid=ShopCart.objects.get(pk=cart_id)
    get_cartid.delete()
    cartlistcount=ShopCart.objects.filter(user=request.user).count()
    return JsonResponse({'status':1,'cartlistcount':cartlistcount})

from .checkcart_sess import Checkcart_sess
def del_cart_sess_no_var(request):
    #get cart session
    cart_sess_no_var=Cartsession_no_var(request)
    #Get p_id from ajax
    p_id=int(request.POST['p_id'])
    #print("get p_id:",p_id)
    cart_sess_no_var.delete_pro_sess_no_var(productid=p_id)
    # Count product in Session or quantiy of items plus with cart list var
    cart_count=cart_sess_no_var.__len__() + Cartsession(request).__len__()
    #call func
    context=Checkcart_sess(request)
    contextajax= context
    context={
        'status':1,
        'product_id':p_id,
        'cartlistcount':cart_count, 
        'rendered_table': render_to_string('cartlistajax_sess.html', contextajax),   # for display at header
    }
    #Return response
    response=JsonResponse(context)
    return response


def del_cart_sess_var(request):
    #get cart session
    cart_sess=Cartsession(request)
    #Get p_id from ajax
    p_id=int(request.POST['p_id'])
    #print("del get p_id:",p_id)
    
    cart_sess.delete_pro_sess(productid=p_id)
    # Count product in Session or quantiy of items plus with cart list no var
    cart_count=cart_sess.__len__() + Cartsession_no_var(request).__len__()
    #call function
    context=Checkcart_sess(request)
    contextajax= context
    #end test
    context={
        'status':1,
        'product_id':p_id,
        'cartlistcount':cart_count, 
        'rendered_table': render_to_string('cartlistajax_sess.html', contextajax),   # for display at header
    }
    #Return response
    response=JsonResponse(context)
    return response

@login_required(login_url='/login')  # Check login
def orderproduct(request): #old form function
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity
    #NO_VAT 0.00
    vat10 = total * decimal.Decimal(0.00)  # convert float to decimal
    grandtotal = total + vat10
    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        # return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............

            data = Order()
            data.first_name = form.cleaned_data['first_name']  # get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.country = form.cleaned_data['country']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.paymentinfo = form.cleaned_data['paymentinfo']
            data.adminnote = form.cleaned_data['adminnote']
            data.userordernote=form.cleaned_data['userordernote']
            data.user_id = current_user.id
            data.total = total
            data.vat10=vat10
            data.grandtotal=grandtotal
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()  # random generate code
            data.code = ordercode
            data.save()  #

            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id  # Order Id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                if rs.product.variant == 'None':
                    detail.price = rs.product.price
                else:
                    detail.price = rs.variant.price
                detail.variant_id = rs.variant_id
                detail.amount = rs.amount
                detail.save()
                # ***Reduce quantity of sold product from Amount of Product
                if rs.product.variant == 'None':
                    product = Product.objects.get(id=rs.product_id)
                    product.amount -= rs.quantity
                    product.save()
                else:

                   # variant = Variants.objects.get(id=rs.product_id) #orginal code
                    variant = Variants.objects.get(id=rs.variant_id) #code form youtube comments
                    variant.quantity -= rs.quantity
                    variant.save()
                # ************ <> *****************
            # record this order history in Order Table so check the code and payment for product delivery and check location for shipping
          #  ShopCart.objects.filter(user_id=current_user.id).delete()  # Clear & Delete user shopcart
            request.session['cart_items'] = 0
            messages.success(request, "Your Order has been completed. Thank you ")
            #**************************add variable to order complete**********
            #current_user = request.user  # Access User Session information
            # orders = Order.objects.filter(user_id=current_user.id)
            # orderitems = OrderProduct.objects.filter(order_id=)

            # testfrom order

            # orders = Order.objects.get(user_id=current_user.id, code=ordercode)
            # orderitems = OrderProduct.objects.filter(id=id, user_id=current_user.id)
            # endtest
          #  print("ordercode:",ordercode)
            orderinfo = Order.objects.filter(user_id=current_user.id,code=ordercode)
           # print("Return:",orderinfo)
           # print("SQL Query:",orderinfo.query)
            order_product = OrderProduct.objects.filter(user_id=current_user.id,order__code=ordercode)
            dateinvoice=datetime.now()
            setting=Setting.objects.get(pk=1)

            context={'category': category, #old code
                     'ordercode': ordercode, # old code
                     'setting':setting,
                     'shopcart': shopcart,
                     'total': total,
                     'vat10': vat10,
                     'grandtotal': grandtotal,
                     'order_product':order_product,
                     'dateinvoice':dateinvoice,
                     'orderinfo': orderinfo,
            }

            #*****************************************************************
            return render(request, 'Order_Completed.html', context)
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")
            #return HttpResponseRedirect("checkout")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'form': form,
               'profile': profile,
               'vat10': vat10,
               'grandtotal': grandtotal,

               }
    return render(request, 'Order_Form.html', context)

#upadate cart by Ajax
@login_required(login_url='/login')  # Check login
def updatecart(request):
    current_user = request.user
    #yourcart = ShopCart.objects.filter(user_id=current_user.id).order_by('id').count()
    cartlist = ShopCart.objects.filter(user_id=current_user.id).order_by('id')
    data ={}
    #if request.is_ajax :
        #getcartid =request.POST.getlist('get_cartid[]')
    getcartid =request.POST.getlist('get_cartid[]')
         
    getval =request.POST.getlist('get_val[]')
        
    res=convertlisttodic(getcartid,getval)
        #print(convertlisttodic(getcartid,getval))
    for x,y in res.items():
        cartlist = ShopCart.objects.get(id=int(x),user_id=current_user.id)
        cartlist.quantity = int(y)
        cartlist.save()
    #add test
    cartlistcount = ShopCart.objects.filter(user_id=current_user.id).order_by('id').count()
    shopcart = ShopCart.objects.filter(user=request.user).order_by('id')
    count = ShopCart.objects.filter(user=request.user).order_by('id').count()
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            if rs.variant is None:
                pass
            else:
                total += rs.variant.price * rs.quantity
    #NO_VAT 0.00
    vat10= total * decimal.Decimal(0.00) # convert float to decimal
    grandtotal=total + vat10
    
    contextajax = {'shopcart': shopcart,
               #'category': category,
               'total': total,
               'vat10': vat10,
               'grandtotal':grandtotal,
               #'coupon_apply_form':coupon_apply_form,
               'count':count,
               }
    #end test
    context={
        'success':True,
        'cartlistcount':cartlistcount, 
        'rendered_table': render_to_string('cartlistajax.html', context=contextajax),   
    }    
    data=context
    return JsonResponse(data)
        
    #data={'status':0}
    #return JsonResponse(data)
    #return JsonResponse(status=200)    
    #getcartid = request.GET.get('get_cartid')
    #getval = []
    #getval = request.GET.get('get_val')
'''    
    print("print-getcart_id:",getcartid)
    print("print-getvalue:",getval)
    print("count",yourcart)
'''   
      
# Python3 code to demonstrate
# conversion of lists to dictionary
# using naive method
 
# initializing lists
'''
    test_keys = getcartid
    test_values = getval
''' 
# Printing original keys-value lists
'''
    print("Original key list is : " + str(test_keys))
    print("Original value list is : " + str(test_values))
''' 
# using naive method
# to convert lists to dictionary
'''    res = {}
    for key in test_keys:
        for value in test_values:
            res[key] = value
            test_values.remove(value)
            break
'''   
# Printing resultant dictionary
'''    print("Resultant dictionary is : " + str(res))
    #assign key to value dictionary
    for x,y in res.items():
        cartlist = ShopCart.objects.get(id=int(x),user_id=current_user.id)
        cartlist.quantity = int(y)
        cartlist.save()
    
    print("Data have been updated!")

    data={
        'status':1,  
    }
    return JsonResponse(data)
'''     
def convertlisttodic(list1,list2):    
    # Python3 code to demonstrate
# conversion of lists to dictionary
# using naive method
 
# initializing lists
    test_keys = list1
    test_values = list2
 
# Printing original keys-value lists
    print("Original key list is : " + str(test_keys))
    print("Original value list is : " + str(test_values))
 
# using naive method
# to convert lists to dictionary
    res = {}
    for key in test_keys:
        for value in test_values:
            res[key] = value
            test_values.remove(value)
            break
   
# Printing resultant dictionary
    print("Resultant dictionary is : " + str(res))
    return res
    
    

    # category = Category.objects.all()
    # # product = Product.objects.get(pk=id)
    # current_user = request.user  # Access user session information
    # shopcart = ShopCart.objects.filter(user_id=current_user.id)
    # profile=UserProfile.objects.get(user_id=current_user.id)
    # total = 0
    # for rs in shopcart:
    #     total += rs.product.price * rs.quantity
    #
    # # images = Images.objects.filter(product_id=id)
    # # comments = Comment.objects.filter(product_id=id, status='True')
    # # return HttpResponse(str(total)) # test total function
    # context = {
    #     # 'product': product,
    #     'shopcart': shopcart,
    #     'category': category,
    #     # 'images': images,
    #     # 'comments': comments,
    #     'total': total,
    #     'profile':profile,
    # }
    # return render(request, 'Order_Form.html', context)


# class UseCouponView(View):
#     def get(self, request, *args, **kwargs):
#         coupon_code = request.GET.get("coupon_code")
#         user = User.objects.get(username=request.user.username)

#        # status = validate_coupon(coupon_code=coupon_code, user=user)
#         if status['valid']:
#             coupon = Coupon.objects.get(code=coupon_code)
#             coupon.use_coupon(user=user)

#             return HttpResponse("OK")

#         return HttpResponse(status['message'])


#for print pdf weasyprint
@staff_member_required
def admin_order_pdf(request,order_id):
	order = get_object_or_404(Order,id=order_id)
	html = render_to_string('invoice_print.html',{'order':order}) #pdf.html for admin change to invoice_print.html
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.id)
	weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
	return response

#for PDF invoice preview for user or customer
#@login_required(login_url='/login')  # Check login
import requests
#from dotenv import load_dotenv
#import os
#load_dotenv
TOKEN=settings.TOKEN
CHAT_ID=settings.CHAT_ID


def generate_pdf(request,ordercode):
    current_user = request.user
    orderinfo = Order.objects.get(code=ordercode)
    order_product = OrderProduct.objects.filter(user_id=current_user.id,order__code=ordercode).order_by('id')
    dateinvoice=datetime.now()
    setting=Setting.objects.get(pk=1)

    context={
            'ordercode': ordercode, # old code
            'setting':setting,
            'order_product':order_product,
            'dateinvoice':dateinvoice,
            'orderinfo': orderinfo,
    }
    html_string = render_to_string('invoice_print.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="order_{}.pdf"'.format(orderinfo)
    #weasyprint.HTML(string=html_string,base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    weasyprint.HTML(string=html_string,base_url=request.build_absolute_uri()).write_pdf(response)
    
    #sent message to Telegram
    #pdf_link=request.build_absolute_uri()
    invoice_print_url="http://localhost:8000/order/invoiceprint/"+ordercode
    today = format(datetime.now())
    message =today+"You Got Order :"+invoice_print_url		 #"Hello message from SOMMA 123 bot"
    urlmsg = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&caption="Somma MSG"'
    re= requests.post(urlmsg)
    print(re.json())
    #end sent
    
    return response



   

#create function for processes varinat size color and size&color
def getvariantsizecolor(var,data):
        #proid=request.POST.get('proid')
        sizeid=var
        colorid=data
        #print(colorid)
        #print(len(colorid))
        j=[]
        for i in colorid.split(","):
            
                j.append(i)
                #print(j)
        #print(j)
        
        for y in j:
            if y == "None":
                twovariants=False
                #print("variant size or color:")
                j.remove("None")
            else:
                twovariants=True
                #print("variants size and color")
                
        if twovariants==False:
            l = [int(k) for k in j]
            #print(l)
            
        else:
            l = [int(k) for k in j]
        #print(j)
        
            
        if sizeid=='Color':
                variantid=j[0]
                variantcolor=j[1]
                print("***Color****")   
                print("variantID:",variantid) 
                print("colorID:",variantcolor) 
                print("***********")
                #variant=Variants.objects.get(id=variantid)
                context=[variantid,variantcolor]
        elif sizeid=='Size':
                variantid=j[0]
                variantsize=j[1]
                print("***Size****")   
                print("VariantID:",variantid) 
                print("SizeID:",variantsize) 
                print("***********")
                #variant=Variants.objects.get(id=variantid)
                context=[variantid,variantsize]
 
        else:
            
                variantid=j[0]
                variantsize=j[1]
                variantcolor=j[2]
                print("****Size and Color***")   
                print(variantid) 
                print(variantsize)
                print(variantcolor)     
                print("***********")
                #variant=Variants.objects.get(id=variantid)
                context=[variantid,variantsize,variantcolor]
        
        print("this is print context:",context)
        return context       
                
                     
from django_simple_coupons.models import Coupon, CouponUser  
from django_simple_coupons import validations               
# apply Promo code to shopcart by ajax    
def promoapply(request):
    data={}
    current_user = request.user
    getpromocode=request.POST.get('get_promocode')
    #print(getpromocode)
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity
    # NO_VAT 0.00
    vat10 = total * decimal.Decimal(0.00)  # convert float to decimal
    grandtotal = total + vat10
    #check code
    checkcoupon=validations.validate_coupon(getpromocode,current_user)
    
    print("checkvalidcode",checkcoupon['valid'])
    if checkcoupon['valid']==True:
        coupon = Coupon.objects.get(code=getpromocode)
        promodiscount=coupon.get_discount()
        #y=coupon.get_discounted_value(promodiscount['value'])
        #print("True coupon discount",promodiscount['is_percentage'],promodiscount['value'])
        #print("apply rule discount ",y)
        #getdiscount=Coupon.get_discount()
        newpriceaftercoupon=coupon.get_discounted_value(total)
        #usecoupon=coupon.use_coupon(current_user) #for user use coupon time
      
       # if usecoupon
        print("New value ",newpriceaftercoupon)
        #print("Your coupon TimeUse apply:",usecoupon)
        #print("Your coupon TimeUse apply:",coupon.times_used) # count use coupon
        contextajax={
            'getpromocode':getpromocode,
            'checkcoupon':checkcoupon,
            'promodiscount':promodiscount,
            'total': total,
            'vat10': vat10,
            'grandtotal': grandtotal,
            'newpriceaftercoupon':newpriceaftercoupon,
            
        }
        context={
            'status':True,
            'rendered_table':render_to_string('ajaxpromoapply.html',context=contextajax),
            'rendered_table_alert':render_to_string('ajaxpromocode.html',{'getpromocode':getpromocode,'checkcoupon':checkcoupon,'promodiscount':promodiscount,}),
            
        }
        # data={'rendered_table':render_to_string('ajaxpromoapply.html',context=context)} 
        # return JsonResponse(data)
       
    else:
        print("Fales Coupon")
        #y="No Discount"
        #promodiscount="value x"
        print(checkcoupon)
        contextajax={
            'getpromocode':getpromocode,
            'checkcoupon':checkcoupon,
        }
        context={
            # 'status':False,
            'rendered_table':render_to_string('ajaxpromocode.html',context=contextajax)
        }
    # data={'rendered_table':render_to_string('ajaxpromocode.html',context=context)}   
    # return JsonResponse(data)
    
    data=context
    
    return JsonResponse(data)


@login_required(login_url='/login')  # Check login
def checkout(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity
    #total_=total
    # NO_VAT 0.00
    vat10 = total * decimal.Decimal(0.00)  # convert float to decimal
    grandtotal = total + vat10             # for 3 digit number '1000.50' to '1,000.50'
    # grandtotal='{:,.2f}'.format(grandtotal_)# for 3 digit number '1000.50' to '1,000.50'
    # total = '{:,.2f}'.format(total_)   
    # vat10 = '{:,.2f}'.format(vat10_)    
    phonefrm = OrderForm()
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'phonefrm': phonefrm,
               'profile': profile,
               'vat10': vat10,
               'grandtotal': grandtotal,

               }
    if shopcart.exists():
        return render(request,'Order_checkout.html',context)
    else:
        messages.info("Your Cart is empty, So please shopping")
        return redirect('/')

def checkout_sess(request):
    checksess=Checkcart_sess(request)
    context=checksess
    phonefrm = OrderForm()
    context.update({
            'phonefrm': phonefrm,
            })  
    return render(request,'Order_checkout.html',context)

        # messages.info("Your Cart is empty, So please shopping")
        # return redirect('/')    


import random
@login_required(login_url='/login')  # Check login
def checkoutcompleted(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    setting=Setting.objects.get(pk=1)
    getrateordered=Paymentlist.objects.get(setting=1)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity
    # NO_VAT 0.00
    vat10 = total * decimal.Decimal(0.00)  # convert float to decimal
    grandtotal = total + vat10
    getcheckcoupon=request.POST.get('checkcouponvalid')
    getpromocodevalide=request.POST.get('getpromocode')# take code valide for count used coupone
    # if getcheckcoupon == 'True': # for check count coupon used
    #     coupon = Coupon.objects.get(code=getpromocodevalide)
    #     usecoupon=coupon.use_coupon(current_user) #for user use coupon time
    #     print("Your have used your coupon",coupon.times_used)
    getis_percentage=request.POST.get('is_percentage')
    getdiscountvalue=request.POST.get('promoapplydiscount')
    getpriceafterdiscount=request.POST.get('priceafterdiscount')
    getvat10afterdiscount= request.POST.get('vat10afterdiscount')
    getgrandtotalafterdiscount=request.POST.get('newpricegrandtotal') 
    print("befor_getis_percentage",getis_percentage)
    print("befor_getdiscountvalue",getdiscountvalue)
    if getis_percentage == 'True':
        getdiscountvalue=float(getdiscountvalue.removesuffix('%'))/100
        print("removesuffix % sign",getdiscountvalue)


    elif getis_percentage == 'False' :
        getdiscountvalue=float(getdiscountvalue.removesuffix('$'))

    else:
        pass    
    print("*******Nornal Order Summary*******")
    print("Total",total)
    print("Vat10",vat10)
    print("grandtotal",grandtotal)
    print("*******Discount Order Summary*******")
    print("getcheckcoupon",getcheckcoupon)
    print("getis_percentage",getis_percentage)
    print("after_getdiscountvalue",getdiscountvalue)
    print("getpriceafterdiscount",getpriceafterdiscount)
    print("getvat10afterdiscount",getvat10afterdiscount)
    print("getgrandtotalafterdiscount",getgrandtotalafterdiscount)
    
    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        # return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............

            data = Order()
            data.first_name = request.POST.get('first_name')  # get product quantity from form
            data.last_name = request.POST.get('last_name')
            data.email = request.POST.get('email')
            data.address = request.POST.get('address')
            #data.phone = request.POST.get('phone')    # -> phone form field for check valid number
            data.phone = form.cleaned_data['phone']
            data.adminnote = request.POST.get('locationlatlng')
            data.userordernote= request.POST.get('useraddnote')
            data.paymentinfo = request.POST.get('paymentinfo')
            data.rate_by_ordered = getrateordered.ratetoday # get recode rate today ordered
            data.user_id = current_user.id
            if getcheckcoupon == 'True': # for check count coupon used
                coupon = Coupon.objects.get(code=getpromocodevalide)
                usecoupon=coupon.use_coupon(current_user) #for user use coupon time
                data.discount = getdiscountvalue  # save value to discount Order 
                data.totalafterdiscount = float(getpriceafterdiscount)
                data.vat10afterdiscount = float(getvat10afterdiscount)
                data.grandtotalafterdiscount = float(getgrandtotalafterdiscount)   
            else:    
                pass
            # if have discount we record the old total 
            data.total = total
            data.vat10 = vat10
            data.grandtotal = grandtotal
            if getgrandtotalafterdiscount == None:   
                data.grandtotal_in_kh_real = float(grandtotal) * float(getrateordered.ratetoday)
            else:
                data.grandtotal_in_kh_real = float(getgrandtotalafterdiscount) * float(getrateordered.ratetoday)
            data.ip = request.META.get('REMOTE_ADDR') # get ip from customer
            ordercode = get_random_string(5).upper()  # random generate code
            data.code = ordercode
            #tracking number
            trackno= "SOMMA"+str(random.randint(11111,99999))
            while Order.objects.filter(tracking_no=trackno) is None:
                trackno= "SOMMA"+str(random.randint(11111,99999))
            data.tracking_no = trackno
            #payment COD
            data.save()  # save info to Order 

            for rs in shopcart:     # save shopcart to OrderProduct for delete shopcart
                detail = OrderProduct()
                detail.order_id = data.id  # Order Id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.variant_id = rs.variant_id
                if rs.product.variant == 'None':
                    detail.price = rs.product.price
                    detail.amount = rs.amount
                else:
                    detail.price = rs.variant.price
                    detail.amount = rs.varamount
            
                # if rs.product.variant == 'None':
                #     detail.amount = rs.amount
                # else:
                #     detail.amount = rs.varamount
                detail.save() # save shopcart to OrderProduct 
                
                # ***Reduce quantity of sold product from Amount of Product
                if rs.product.variant == 'None':
                    product = Product.objects.get(id=rs.product_id)
                    product.amount -= rs.quantity
                    product.save()
                else:

                    # variant = Variants.objects.get(id=rs.product_id) #orginal code
                    variant = Variants.objects.get(id=rs.variant_id) #code form youtube comments
                    variant.quantity -= rs.quantity
                    variant.save()
                # ************ <> *****************
                # record this order history in Order Table so check the code and payment for product delivery and check location for shipping
            
            # Clear & Delete user shopcart
            ShopCart.objects.filter(user_id=current_user.id).delete()  # Clear & Delete user shopcart
            #request.session['cart_items'] = 0
            # -> save invoice in to PDF file , that file name with invoice ID username and phone and date
            # -> sent PDF to telegram group for make call and payment
            
            messages.success(request, "Your Order has been completed. Thank you for your Order ")
            
            
                #**************************add variable to order complete**********
                #current_user = request.user  # Access User Session information
                # orders = Order.objects.filter(user_id=current_user.id)
                # orderitems = OrderProduct.objects.filter(order_id=)

                # testfrom order

                # orders = Order.objects.get(user_id=current_user.id, code=ordercode)
                # orderitems = OrderProduct.objects.filter(id=id, user_id=current_user.id)
                # endtest
            #  print("ordercode:",ordercode)
            #orderinfo = Order.objects.filter(user_id=current_user.id,code=ordercode).order_by('id')
            orderinfo = Order.objects.get(code=ordercode)
            #print("orderinfo:",orderinfo)
            # print("SQL Query:",orderinfo.query)
            order_product = OrderProduct.objects.filter(user_id=current_user.id,order__code=ordercode).order_by('id')
            #print("OrderProduct",order_product)
            dateinvoice=datetime.now()
            #setting=Setting.objects.get(pk=1)

            context={
                    #'category': category, #old code
                    'ordercode': ordercode, # old code
                    'setting':setting,
                    #'shopcart': shopcart,
                    #'total': total,
                    #'vat10': vat10,
                    #'grandtotal': grandtotal,
                    'order_product':order_product,
                    'dateinvoice':dateinvoice,
                    'orderinfo': orderinfo,
            }

                #*****************************************************************
            #return render(request, 'Order_checkoutcompleted.html', context)
            return HttpResponseRedirect(reverse_lazy('order:checkoutcompleted_2', args=(ordercode,)))
            #return HttpResponseRedirect(reverse('order:invoiceprint', args=(ordercode,)))
        else:
            phonenum=request.POST['phone']
            print("***invalid phone",phonenum)
            form=OrderForm()
            messages.info(request,"invalid form phone number")
            return HttpResponseRedirect(reverse_lazy('order:checkout')) 
    elif ShopCart.objects.filter(user_id=current_user.id).exists():
        messages.warning(request, "you errors please checkout again or contact us")
        #form = OrderForm()    # add
        messages.info(request, "Please input valide phone number that use with telegram or whatapp ")
        return HttpResponseRedirect(reverse_lazy('order:checkout')) # add phonefrm
    # elif Order.objects.filter(user_id=current_user.id,code=ordercode).exists():
    #     messages.info(request,"your order completed and check your invoice")
    #     return HttpResponseRedirect(reverse('order:invoiceprint', args=(ordercode,)))
    else:
        form = OrderForm()    # add
        messages.info(request,"Please check you account for your order, And continues shopping!")
        return HttpResponseRedirect(reverse_lazy('order:checkout'))
        #return HttpResponseRedirect('/')
    
    #return HttpResponseRedirect(/)
    
    
@login_required(login_url='/login')  # Check login    
def checkoutcompleted_2(request,ordercode): # for refresh page test
    current_user = request.user
    orderinfo = Order.objects.get(user_id=current_user.id,code=ordercode)
    print("orderinfo:",orderinfo)
    # print("SQL Query:",orderinfo.query)
    order_product = OrderProduct.objects.filter(user_id=current_user.id,order__code=ordercode)
    dateinvoice=datetime.now()
    setting=Setting.objects.get(pk=1)
    paymentrate=Paymentlist.objects.get(setting=1)

    context={
            #'category': category, #old code
            'ordercode': ordercode, # old code
            'setting':setting,
            #'shopcart': shopcart,
            #'total': total,
            #'vat10': vat10,
            #'grandtotal': grandtotal,
            'order_product':order_product,
            'dateinvoice':dateinvoice,
            'orderinfo': orderinfo,
            'paymentrate':paymentrate,
    }

    #*****sent message to telegram************************************************************
    # invoice_print_url="http://localhost:8000/order/invoiceprint/"+ordercode
    # today = format(datetime.now())
    # message =today+"You Got Order :"+invoice_print_url		 #"Hello message from SOMMA 123 bot"
    # urlmsg = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&caption="Somma MSG"'
    # re= requests.post(urlmsg)
    # print(re.json())    
    #*****End sent message to telegram*********
    
    return render(request, 'Order_checkoutcompleted.html', context)
    
def testfrmcompleted(request):
    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST or None,initial={'phone':"077263362"})
        # return HttpResponse(request.POST.items())
        if form.is_valid():
            phonenum=form.cleaned_data['phone']
            print("print valid phone",phonenum)
            print(form)
            messages.success(request, "Your phone number is valid ")
        else:
            phonenum=request.POST['phone']
            print("***invalid phone",phonenum)
            messages.info(request,"invalid form phone number")
    else:        
        form = OrderForm(initial={'phone':"077263362"})    
        print(form)
        messages.info(request, "Please input valide phone number that use with telegram or whatapp ")
    return render(request,'Order_checkout.html',{'phonefrm':form,})         
        

def invoiceprint(request,ordercode):
    current_user = request.user
    orderinfo = Order.objects.get(code=ordercode)
    print("orderinfo:",orderinfo)
    # print("SQL Query:",orderinfo.query)
    order_product = OrderProduct.objects.filter(user_id=current_user.id,order__code=ordercode).order_by('id')
    #dateinvoice=datetime.now()
    setting=Setting.objects.get(pk=1)

    context={
           
            'ordercode': ordercode, # old code
            'setting':setting,
            'order_product':order_product,
            #'dateinvoice':dateinvoice,
            'orderinfo': orderinfo,
    }

    return render(request,'invoice_print.html',context)

def receiptprint(request,ordercode):
    current_user = request.user
    orderinfo = Order.objects.get(code=ordercode)
    print("orderinfo:",orderinfo)
    # print("SQL Query:",orderinfo.query)
    order_product = OrderProduct.objects.filter(user_id=current_user.id,order__code=ordercode).order_by('id')
    #dateinvoice=datetime.now()
    setting=Setting.objects.get(pk=1)

    context={
           
            'ordercode': ordercode, # old code
            'setting':setting,
            'order_product':order_product,
            #'dateinvoice':dateinvoice,
            'orderinfo': orderinfo,
    }

    return render(request,'print_receipt.html',context)

def invoiceprint_2(request,ordercode): # just check invoice code with NO current user
    #current_user = request.user
    orderinfo = Order.objects.get(code=ordercode)
    print("orderinfo:",orderinfo)
    # print("SQL Query:",orderinfo.query)
    order_product = OrderProduct.objects.filter(order__code=ordercode).order_by('id')
    dateinvoice=datetime.now()
    setting=Setting.objects.get(pk=1)

    context={
           
            'ordercode': ordercode, # old code
            'setting':setting,
            'order_product':order_product,
            'dateinvoice':dateinvoice,
            'orderinfo': orderinfo,
    }

    return render(request,'invoice_print.html',context)

from .telegram_sent_test import sent_to_telegram
from .utils import sent_otp
import pyotp
def checkphone(request):
    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST) # bring only phonefield
        phonenum = request.POST.get('phone')
        # return HttpResponse(request.POST.items())
        if form.is_valid():
            #phonenum=form.cleaned_data['phone']
            
            print("print valid phone",phonenum)
            print(form)
            #messages.info(request, "Your phone number is valid")
            #messages.info(request,"Please add your phone again!")
            #sent one time passowrd
            #........
            codeotp=sent_otp(request,phonenum) # sent OTP code
            print("codeotp:",codeotp)
            #check 
            sent_to_telegram(codeotp,phonenum) # take OTPcode and phonenumber to telegram for user manual sent to User Phone
            request.session['phonenum']=phonenum
            return redirect('order:otp_phone') # otp_phone otpverify code
        else:
            phonenum=request.POST['phone']
            print("***invalid phone",phonenum)
            messages.info(request,"invalid form phone number")
    else:        
        form = OrderForm()    
        print(form)
        messages.info(request, "Please input valid phone number that use with telegram or whatapp ")
    return render(request,'Order_checkout.html',{'phonefrm':form,}) 

def otp_view(request):
    error_message=None
    if request.method == 'POST':
        otp = request.POST.get('otp')
        print("Your otp verify submit code:",otp)
        phonenum = request.session['phonenum']
        print("phonenum:",phonenum)
        otp_secret_key=request.session['otp_secret_key']
        otp_valid_until=request.session['otp_valid_date']
        print("otpsecretkey",otp_secret_key)
        print("otp valide until",otp_valid_until)
        if otp_secret_key and otp_valid_until is not None:
            valid_until = datetime.fromisoformat(otp_valid_until)
            if valid_until > datetime.now():
                totp=pyotp.TOTP(otp_secret_key,interval=180)
                if totp.verify(otp,valid_window=60): #valid_window=7 for time available in windows
                    # user= get_object_or_404(User,username=username_)
                    # login(request,user)
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    messages.info(request,"Successful,Valid phone number")
                    if request.user.is_authenticated:
                        return redirect('order:checkout')
                    else:
                        return redirect('order:checkout_sess')
                    
                else:
                    error_message="Invalid Verify OTP Code !"
                    
            else:
                error_message="OTP Verify Code has expired"
                del request.session['phonenum']
                messages.info(request,"OTP Verify Code has expired. Please add phone number again")
                if request.user.is_authenticated:
                    return redirect('order:checkout')
                else:
                    return redirect('order:checkout_sess')
                
        else:
            error_message="Something wrong!" 
            del request.session['phonenum']       

    return render(request,'otp_phone.html',{'error_message':error_message}) 

#add to cart with Session , No_varinat
from .cart_session import Cartsession,Cartsession_no_var

def add_cart_session_no_var(request):
    #get cart session
    cart_sess=Cartsession_no_var(request)
    #Get p_id from ajax
    p_id=int(request.GET['p_id'])
    p_qty=int(request.GET['p_qty'])
    # Lookup product in DB
    get_product = get_object_or_404(Product,id=p_id)
    #check in Cart Sess no_var
    checkcart=cart_sess.check_pid_in_cart_no_var(p_id)
    print("CheckCartNOVAR:",checkcart)
    if checkcart == False:
        # Save to Session
        cart_sess.add_no_var(product=get_product,qty=p_qty)
        print("add to cart")
        #messages.info(request,"Product added to cart")
    else:
        
        print("already in cart")
        #messages.info(request,"Product already in cart!")
    # Count product in Session or quantiy of items
    cart_count=cart_sess.__len__() + Cartsession(request).__len__()
    
    #Return response
    #call func checkcart_sess
    context_1=Checkcart_sess(request)
    contextajax= context_1
    
    context={
        'bool':True,
        'product_id':get_product.id,
        'cartlistcount_sess':cart_count,
        'rendered_table': render_to_string('cartlistajax_sess.html', contextajax),   # for display at header
    }
    response=JsonResponse(context)
    return response


#add to cart with Session with  Varinat
def add_cart_session_var(request):
    #get cart session
    cart_sess=Cartsession(request)
    p_id=int(request.GET['pid'])
    p_qty=int(request.GET['qty'])
    varid=int(request.GET['varid'])
    # Lookup product in DB variants
    get_product_var = get_object_or_404(Variants,product=p_id,id=varid)
    checkcart=cart_sess.check_pid_in_cart_var(p_id)
    print("CheckCartVAR:",checkcart)
    if checkcart == False:
        # Save to Session
        cart_sess.add_var(product=get_product_var.product.id,qty=p_qty,varid=varid)
        print("add to cart")
    else:
        #messages.info("already in cart")   
        print("already in cart")
    
    print("cart session var",cart_sess)
    print("Var Pro id session var",get_product_var.product.id)
    #check if already in Cart or Not
    # if get_product_var:
    #     print("You have already in Cart Session")
    # Count product in Session or quantiy of items
    cart_count=cart_sess.__len__() + Cartsession_no_var(request).__len__()
    #Return response
    #call func checkcart_sess
    context=Checkcart_sess(request)
    contextajax= context
    context={
        'bool':True,
        'product_id':get_product_var.product.id,
        'cartlistcount_sess':cart_count,
        'rendered_table': render_to_string('cartlistajax_sess.html', contextajax),   # for display at header
    }
    response=JsonResponse(context)
    return response
    
# request cartlist by session header    
def view_cartlist_sess(request):
    #Get wishlist
    check_cart_sess =''
     
    cart_list_sess_prods=Cartsession(request)
    cart_list_sess_no_var=Cartsession_no_var(request)
    #cart_sess_products_var=cart_list_sess_prods.cart_list_session_var
    
    if cart_list_sess_prods and not cart_list_sess_no_var:
        check_cart_sess = 'cart_var'
        cart_sess_products_var=cart_list_sess_prods.cart_list_session_var
        cart_pro_qty=cart_list_sess_prods.get_qty_var
        cartcount_sess=cart_list_sess_prods.__len__()
        #print("cart_sess_products_var:",cart_list_sess_prods)
        gettotal_var=cart_list_sess_prods.get_total_var
        context={
            'count_sess':cartcount_sess,
            'check_cart_sess':check_cart_sess,
            'cart_sess_products_var':cart_sess_products_var,
            'cart_pro_qty': cart_pro_qty,
            'grandtotal_sess':gettotal_var,
        
        }
        
    elif cart_list_sess_no_var  and not cart_list_sess_prods :
        check_cart_sess = 'cart_no_var'
        cart_list_sess_prods_no_var=cart_list_sess_no_var.cart_list_session_no_var
        cart_pro_qty_no_var=cart_list_sess_no_var.get_qty_no_var
        cartcount_sess=cart_list_sess_no_var.__len__()
        gettotal_no_var=cart_list_sess_no_var.get_total_no_var
        context={
            'count_sess':cartcount_sess,
            'check_cart_sess':check_cart_sess,
            'cart_list_sess_prods_no_var':cart_list_sess_prods_no_var,
            'cart_pro_qty_no_var':cart_pro_qty_no_var,
            'grandtotal_sess':gettotal_no_var,
        }
    
    elif cart_list_sess_prods and cart_list_sess_no_var:
        check_cart_sess = 'both'
        cart_sess_products_var=cart_list_sess_prods.cart_list_session_var
        cart_pro_qty=cart_list_sess_prods.get_qty_var
        cart_list_sess_prods_no_var=cart_list_sess_no_var.cart_list_session_no_var
        cart_pro_qty_no_var=cart_list_sess_no_var.get_qty_no_var
        cartcount_sess=cart_list_sess_prods.__len__() + cart_list_sess_no_var.__len__()
        gettotal_var=cart_list_sess_prods.get_total_var()
        gettotal_no_var=cart_list_sess_no_var.get_total_no_var()
        grandtotal_sess=gettotal_var + gettotal_no_var
        context={
            'count_sess':cartcount_sess,
            'check_cart_sess':check_cart_sess,
            'cart_sess_products_var':cart_sess_products_var,
            'cart_pro_qty': cart_pro_qty,
            'cart_list_sess_prods_no_var':cart_list_sess_prods_no_var,
            'cart_pro_qty_no_var':cart_pro_qty_no_var,
            'grandtotal_sess':grandtotal_sess,
        }
        
    else:
        #messages.info(request,"don't have cart in session")
        context={ 
            #'check_cart_sess': check_cart_sess,
        
        }
    return render(request,'shopcart_products.html',context)

def updatecart_sess(request):
    data ={}
    getcartid =request.POST.getlist('get_cartid[]')
    getval =request.POST.getlist('get_val[]')
    res=convertlisttodic(getcartid,getval)
    print("RES DIC:",res)
    #1 res here the new dic
    #2update to session
    #3 get the session var and no var
    #4 if check session var 
    check_cart_sess =''
    cart_list_sess_prods=Cartsession(request)
    cart_list_sess_no_var=Cartsession_no_var(request)
    if cart_list_sess_prods and not cart_list_sess_no_var:
        check_cart_sess = 'cart_var'
        
        get_old_cartlist_var=cart_list_sess_prods.get_qty_var()
        #update the old
        #get_old_cartlist_var.update(res)
        print("Befor have Var :",get_old_cartlist_var)
        cart_list_sess_prods.updatecart_var(res)
        print("after have Var :",cart_list_sess_prods)
        #after update:
        cartcount_sess=cart_list_sess_prods.__len__()
        cart_sess_products_var=cart_list_sess_prods.cart_list_session_var
        cart_pro_qty=cart_list_sess_prods.get_qty_var
        gettotal_var=cart_list_sess_prods.get_total_var
        context={
            'count_sess':cartcount_sess,
            'check_cart_sess':check_cart_sess,
            'cart_sess_products_var':cart_sess_products_var,
            'cart_pro_qty': cart_pro_qty,
            'grandtotal_sess':gettotal_var,
        }
    elif cart_list_sess_no_var  and not cart_list_sess_prods : 
        check_cart_sess = 'cart_no_var'
        
        get_old_cartlist_no_var=cart_list_sess_no_var.get_qty_no_var()
        #update the old
        # get_old_cartlist_no_var.update(res)
        print("Before have NO_Var: ",get_old_cartlist_no_var)
        cart_list_sess_no_var.updatecart_no_var(res)
        print("Before have NO_Var: ",cart_list_sess_no_var)
        #after updated
        cartcount_sess=cart_list_sess_no_var.__len__()
        cart_list_sess_prods_no_var=cart_list_sess_no_var.cart_list_session_no_var
        cart_pro_qty_no_var=cart_list_sess_no_var.get_qty_no_var
        gettotal_no_var=cart_list_sess_no_var.get_total_no_var
        #print("gettotal_no_var:",gettotal_no_var)
        context={
            'count_sess':cartcount_sess,
            'check_cart_sess':check_cart_sess,
            'cart_list_sess_prods_no_var':cart_list_sess_prods_no_var,
            'cart_pro_qty_no_var':cart_pro_qty_no_var,
            'grandtotal_sess':gettotal_no_var,
        }
    elif cart_list_sess_prods and cart_list_sess_no_var:
        check_cart_sess = 'both'
        
        #get_old_cartlist_var=cart_list_sess_prods.get_var_qty()
        #get_qty_var
        get_old_cartlist_var_pid=cart_list_sess_prods.get_qty_var()
        print("beforupdate Var PID:",get_old_cartlist_var_pid)
        cart_list_sess_prods.updatecart_var(res)
        print("after update Var PID:",cart_list_sess_prods)
        
        # and then update the no_var
        get_old_cartlist_no_var=cart_list_sess_no_var.get_qty_no_var()
        print("beforupdate no var:",get_old_cartlist_no_var)
        #get_old_cartlist_no_var.update(res)
        cart_list_sess_no_var.updatecart_no_var(res)
        print("afterupdate no var:",cart_list_sess_no_var)
        #after updated
        cartcount_sess=cart_list_sess_prods.__len__() + cart_list_sess_no_var.__len__()
        cart_sess_products_var=cart_list_sess_prods.cart_list_session_var
        cart_pro_qty=cart_list_sess_prods.get_qty_var
        gettotal_var=cart_list_sess_prods.get_total_var()
        
        cart_list_sess_prods_no_var=cart_list_sess_no_var.cart_list_session_no_var
        cart_pro_qty_no_var=cart_list_sess_no_var.get_qty_no_var
        gettotal_no_var=cart_list_sess_no_var.get_total_no_var()
        grandtotal_sess=gettotal_var + gettotal_no_var
        context={
            'count_sess':cartcount_sess,
            'check_cart_sess':check_cart_sess,
            'cart_sess_products_var':cart_sess_products_var,
            'cart_pro_qty': cart_pro_qty,
            'cart_list_sess_prods_no_var':cart_list_sess_prods_no_var,
            'cart_pro_qty_no_var':cart_pro_qty_no_var,
            'grandtotal_sess':grandtotal_sess,
           
        }

    # for x,y in res.items():
    #     print("x,y:",x,y)
    contextajax = context
    #end test
    context_sess={
        'success':True,
        'cartlistcount':'cartlistcount', 
        'rendered_table': render_to_string('cartlistajax_sess.html', context=contextajax),   
    }    
    data=context_sess
    return JsonResponse(data)


def header_cartlist_sess(request):
    #check if user login : if user login session not request else request session
    check_cart_sess =''
    if request.user.is_authenticated:
        # contextajax= context
        print("user has login")
        context={
            'bool':False,
        # 'cartlistcount_sess':cart_count,
            # 'rendered_table': render_to_string('cartlistajax_sess.html', contextajax),   # for display at header
        }
        response=JsonResponse(context)
        return response
    #     return 
    else: # Not authenticath 
        if request.is_ajax:
            print("Request Ajax")
            cart_list_sess_prods=Cartsession(request)
            cart_list_sess_no_var=Cartsession_no_var(request)
            #cart_sess_products_var=cart_list_sess_prods.cart_list_session_var
        
            if cart_list_sess_prods and not cart_list_sess_no_var:
                check_cart_sess = 'cart_var'
                cart_sess_products_var=cart_list_sess_prods.cart_list_session_var
                cart_pro_qty=cart_list_sess_prods.get_qty_var
                cartcount_sess=cart_list_sess_prods.__len__()
                #print("cart_sess_products_var:",cart_list_sess_prods)
                gettotal_var=cart_list_sess_prods.get_total_var
                context={
                    'count_sess':cartcount_sess,
                    'check_cart_sess':check_cart_sess,
                    'cart_sess_products_var':cart_sess_products_var,
                    'cart_pro_qty': cart_pro_qty,
                    'grandtotal_sess':gettotal_var,
                
                }
                
            elif cart_list_sess_no_var  and not cart_list_sess_prods :
                check_cart_sess = 'cart_no_var'
                cart_list_sess_prods_no_var=cart_list_sess_no_var.cart_list_session_no_var
                cart_pro_qty_no_var=cart_list_sess_no_var.get_qty_no_var
                cartcount_sess=cart_list_sess_no_var.__len__()
                gettotal_no_var=cart_list_sess_no_var.get_total_no_var
                context={
                    'count_sess':cartcount_sess,
                    'check_cart_sess':check_cart_sess,
                    'cart_list_sess_prods_no_var':cart_list_sess_prods_no_var,
                    'cart_pro_qty_no_var':cart_pro_qty_no_var,
                    'grandtotal_sess':gettotal_no_var,
                }
            
            elif cart_list_sess_prods and cart_list_sess_no_var:
                check_cart_sess = 'both'
                cart_sess_products_var=cart_list_sess_prods.cart_list_session_var
                cart_pro_qty=cart_list_sess_prods.get_qty_var
                cart_list_sess_prods_no_var=cart_list_sess_no_var.cart_list_session_no_var
                cart_pro_qty_no_var=cart_list_sess_no_var.get_qty_no_var
                cartcount_sess=cart_list_sess_prods.__len__() + cart_list_sess_no_var.__len__()
                gettotal_var=cart_list_sess_prods.get_total_var()
                gettotal_no_var=cart_list_sess_no_var.get_total_no_var()
                grandtotal_sess=gettotal_var + gettotal_no_var
                context={
                    'count_sess':cartcount_sess,
                    'check_cart_sess':check_cart_sess,
                    'cart_sess_products_var':cart_sess_products_var,
                    'cart_pro_qty': cart_pro_qty,
                    'cart_list_sess_prods_no_var':cart_list_sess_prods_no_var,
                    'cart_pro_qty_no_var':cart_pro_qty_no_var,
                    'grandtotal_sess':grandtotal_sess,
                }
                
            else:
                #messages.info(request,"don't have cart in session")
                context={ 
                    #'check_cart_sess': check_cart_sess,
                
                }
            contextajax= context
            context={
                'bool':True,
            # 'cartlistcount_sess':cart_count,
                'rendered_table': render_to_string('cartlistajax_sess.html', contextajax),   # for display at header
            }
            response=JsonResponse(context)
            return response
        else:  # not Ajax request
            return HttpResponseBadRequest('Invalid request Sess')  
    
    
    
import random
def checkoutcompleted_sess(request):
    current_user = int(4)
    # shopcart = ShopCart.objects.filter(user_id=current_user.id)
    setting=Setting.objects.get(pk=1)
    getrateordered=Paymentlist.objects.get(setting=1)
    vat10= 0.00
    
    checksess=Checkcart_sess(request)
    #context=checksess
    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        # return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............

            data = Order()
            data.first_name = request.POST.get('first_name')  # get product quantity from form
            data.last_name = request.POST.get('last_name')
            data.email = request.POST.get('email')
            data.address = request.POST.get('address')
            #data.phone = request.POST.get('phone')    # -> phone form field for check valid number
            data.phone = form.cleaned_data['phone']
            data.adminnote = request.POST.get('locationlatlng')
            data.userordernote= request.POST.get('useraddnote')
            data.paymentinfo = request.POST.get('paymentinfo')
            data.rate_by_ordered = getrateordered.ratetoday # get recode rate today ordered
            data.user_id = current_user
            
            if checksess['check_cart_sess'] == 'cart_var':
                data.total = Cartsession(request).get_total_var() #checksess['grandtotal_sess']
                data.vat10 = vat10
                data.grandtotal = Cartsession(request).get_total_var() #checksess['grandtotal_sess']
                #if getgrandtotalafterdiscount == None:   
                data.grandtotal_in_kh_real = Cartsession(request).get_total_var() * float(getrateordered.ratetoday)
            elif checksess['check_cart_sess'] == 'cart_no_var':
                    data.total = Cartsession_no_var(request).get_total_no_var() #checksess['grandtotal_sess']
                    data.vat10 = vat10
                    data.grandtotal = Cartsession_no_var(request).get_total_no_var()#checksess['grandtotal_sess']
                    #if getgrandtotalafterdiscount == None:   
                    data.grandtotal_in_kh_real = Cartsession_no_var(request).get_total_no_var() * float(getrateordered.ratetoday)
            elif checksess['check_cart_sess'] == 'both' :
                data.total = Cartsession(request).get_total_var() + Cartsession_no_var(request).get_total_no_var()
                data.vat10 = vat10
                data.grandtotal = Cartsession(request).get_total_var() + Cartsession_no_var(request).get_total_no_var()
                grandtotal = Cartsession(request).get_total_var() + Cartsession_no_var(request).get_total_no_var()
                #if getgrandtotalafterdiscount == None:   
                data.grandtotal_in_kh_real = grandtotal * float(getrateordered.ratetoday)
                   
            #     data.grandtotal_in_kh_real = float(getgrandtotalafterdiscount) * float(getrateordered.ratetoday)
            data.ip = request.META.get('REMOTE_ADDR') # get ip from customer
            ordercode = get_random_string(5).upper()  # random generate code
            data.code = ordercode
            #tracking number
            trackno= "SOMMA_SESS"+str(random.randint(11111,99999))
            while Order.objects.filter(tracking_no=trackno) is None:
                trackno= "SOMMA_SESS"+str(random.randint(11111,99999))
            data.tracking_no = trackno
            #payment COD
            data.save()  # save info to Order 
            
            if checksess['check_cart_sess'] == 'cart_var':
                #for rs in shopcart:     # save shopcart to OrderProduct for delete shopcart
                for rs in Cartsession(request).cart_list_session_var():#checksess['cart_sess_products_var']:   
                    print("RS**pid",rs.id)
                    detail = OrderProduct()
                    # detail.order_id = data.id  # Order Id
                    # detail.product_id = rs.product.id
                    for key, values in Cartsession(request).get_var_qty().items(): #checksess['cart_pro_qty'].items : 
                        print("Key Pid:** and values",int(key),values)
                        if int(key) == rs.id:
                            detail.quantity = int(values)
                            qty=int(values)
                            detail.price = rs.price
                            detail.amount = rs.price * qty #rs.varamount
                            detail.variant_id = rs.id
                            detail.order_id = data.id  # Order Id
                            detail.product_id = rs.product.id
                            detail.user_id = current_user
                            detail.save()
                            # ***Reduce quantity of sold product from Amount of Product
                            variant = Variants.objects.get(id=rs.id) #code form youtube comments
                            variant.quantity -= qty
                            variant.save()   
            elif checksess['check_cart_sess'] == 'cart_no_var':
                for rs in Cartsession_no_var(request).cart_list_session_no_var() :#checksess['cart_list_sess_prods_no_var']:    
                    print("RS NO Var",rs.id)
                    detail = OrderProduct()
                    # detail.order_id = data.id  # Order Id
                    # detail.product_id = rs.id
                    for key, values in Cartsession_no_var(request).get_qty_no_var().items():#checksess['cart_pro_qty_no_var'].items : 
                        print("Key values NO VAR",key,values)
                        if int(key) == rs.id:
                            detail.quantity = int(values)
                            qty=int(values)
                            detail.order_id = data.id  # Order Id
                            detail.product_id = rs.id
                            detail.price = rs.price
                            detail.amount = rs.price * qty #rs.varamount 
                            detail.user_id = current_user    
                            detail.save() # save shopcart to OrderProduct  
                            # ***Reduce quantity of sold product from Amount of Product
                            product = Product.objects.get(id=rs.id)
                            product.amount -= qty
                            product.save() 
            elif checksess['check_cart_sess'] == 'both' :
                #x=checksess['cart_sess_products_var']
                #y=Cartsession(request).cart_list_session_var()
                for rs in Cartsession(request).cart_list_session_var():#checksess['cart_sess_products_var']:   
                    print("RS**pid",rs.id)
                    detail = OrderProduct()
                    # detail.order_id = data.id  # Order Id
                    # detail.product_id = rs.product.id
                    for key, values in Cartsession(request).get_var_qty().items(): #checksess['cart_pro_qty'].items : 
                        print("Key Pid:** and values",int(key),values)
                        if int(key) == rs.id:
                            detail.quantity = int(values)
                            qty=int(values)
                            detail.price = rs.price
                            detail.amount = rs.price * qty #rs.varamount
                            detail.variant_id = rs.id
                            detail.order_id = data.id  # Order Id
                            detail.product_id = rs.product.id
                            detail.user_id = current_user
                            detail.save()
                            # ***Reduce quantity of sold product from Amount of Product
                            variant = Variants.objects.get(id=rs.id) #code form youtube comments
                            variant.quantity -= qty
                            variant.save()    
                    
                for rs in Cartsession_no_var(request).cart_list_session_no_var() :#checksess['cart_list_sess_prods_no_var']:    
                    print("RS NO Var",rs.id)
                    detail = OrderProduct()
                    # detail.order_id = data.id  # Order Id
                    # detail.product_id = rs.id
                    for key, values in Cartsession_no_var(request).get_qty_no_var().items():#checksess['cart_pro_qty_no_var'].items : 
                        print("Key values NO VAR",key,values)
                        if int(key) == rs.id:
                            detail.quantity = int(values)
                            qty=int(values)
                            detail.order_id = data.id  # Order Id
                            detail.product_id = rs.id
                            detail.price = rs.price
                            detail.amount = rs.price * qty #rs.varamount 
                            detail.user_id = current_user    
                            detail.save() # save shopcart to OrderProduct  
                            # ***Reduce quantity of sold product from Amount of Product
                            product = Product.objects.get(id=rs.id)
                            product.amount -= qty
                            product.save()
                            
                    
            # ************ <> *****************
            # record this order history in Order Table so check the code and payment for product delivery and check location for shipping
        
            # Clear & Delete user shopcart
            #ShopCart.objects.filter(user_id=current_user.id).delete()  # Clear & Delete user shopcart
            #request.session['cart_items'] = 0
            # -> save invoice in to PDF file , that file name with invoice ID username and phone and date
            # -> sent PDF to telegram group for make call and payment
            
            #Deleted session after save success
            #del request.session['your key']
            del request.session['cartsess_key']
            del request.session['cartsess_key_no_var']
            del request.session['phonenum']
            
            messages.success(request, "Your Order has been completed. Thank you for your Order ")
            
            
                #**************************add variable to order complete**********
                #current_user = request.user  # Access User Session information
                # orders = Order.objects.filter(user_id=current_user.id)
                # orderitems = OrderProduct.objects.filter(order_id=)

                # testfrom order

                # orders = Order.objects.get(user_id=current_user.id, code=ordercode)
                # orderitems = OrderProduct.objects.filter(id=id, user_id=current_user.id)
                # endtest
            #  print("ordercode:",ordercode)
            #orderinfo = Order.objects.filter(user_id=current_user.id,code=ordercode).order_by('id')
            orderinfo = Order.objects.get(code=ordercode)
            #print("orderinfo:",orderinfo)
            # print("SQL Query:",orderinfo.query)
            order_product = OrderProduct.objects.filter(order__code=ordercode).order_by('id')
            #print("OrderProduct",order_product)
            dateinvoice=datetime.now()
            #setting=Setting.objects.get(pk=1)

            context={
                    #'category': category, #old code
                    'ordercode': ordercode, # old code
                    'setting':setting,
                    #'shopcart': shopcart,
                    #'total': total,
                    #'vat10': vat10,
                    #'grandtotal': grandtotal,
                    'order_product':order_product,
                    'dateinvoice':dateinvoice,
                    'orderinfo': orderinfo,
            }

                #*****************************************************************
            #return render(request, 'Order_checkoutcompleted.html', context)
            return HttpResponseRedirect(reverse_lazy('order:checkoutcompleted_2_sess', args=(ordercode,)))
            #return HttpResponseRedirect(reverse('order:invoiceprint', args=(ordercode,)))
        else:
            phonenum=request.POST['phone']
            print("***invalid phone",phonenum)
            form=OrderForm()
            messages.info(request,"invalid form phone number")
            return HttpResponseRedirect(reverse_lazy('order:checkout_sess')) 
    #elif ShopCart.objects.filter(user_id=current_user.id).exists():
    # else:
    #     messages.warning(request, "you errors please checkout again or contact us")
    #     #form = OrderForm()    # add
    #     messages.info(request, "Please input valide phone number that use with telegram or whatapp ")
    #     return HttpResponseRedirect(reverse_lazy('order:checkout')) # add phonefrm
    # elif Order.objects.filter(user_id=current_user.id,code=ordercode).exists():
    #     messages.info(request,"your order completed and check your invoice")
    #     return HttpResponseRedirect(reverse('order:invoiceprint', args=(ordercode,)))
    else:
        form = OrderForm()    # add
        messages.info(request,"Please check you account for your order, And continues shopping!")
        return HttpResponseRedirect(reverse_lazy('order:checkout_sess'))
        #return HttpResponseRedirect('/')
    
    #return HttpResponseRedirect(/)    
    
# @login_required(login_url='/login')  # Check login    
def checkoutcompleted_2_sess(request,ordercode): # for refresh page test
    # current_user = request.user
    orderinfo = Order.objects.get(code=ordercode)
    print("orderinfo:",orderinfo)
    # print("SQL Query:",orderinfo.query)
    order_product = OrderProduct.objects.filter(order__code=ordercode)
    dateinvoice=datetime.now()
    setting=Setting.objects.get(pk=1)
    paymentrate=Paymentlist.objects.get(setting=1)

    context={
            #'category': category, #old code
            'ordercode': ordercode, # old code
            'setting':setting,
            #'shopcart': shopcart,
            #'total': total,
            #'vat10': vat10,
            #'grandtotal': grandtotal,
            'order_product':order_product,
            'dateinvoice':dateinvoice,
            'orderinfo': orderinfo,
            'paymentrate':paymentrate,
    }

    #*****sent message to telegram************************************************************
    # invoice_print_url="http://localhost:8000/order/invoiceprint/"+ordercode
    # today = format(datetime.now())
    # message =today+"You Got Order :"+invoice_print_url		 #"Hello message from SOMMA 123 bot"
    # urlmsg = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&caption="Somma MSG"'
    # re= requests.post(urlmsg)
    # print(re.json())    
    #*****End sent message to telegram*********
    
    return render(request, 'Order_checkoutcompleted.html', context)

def receiptprint_sess(request,ordercode):
    current_user = int(4)
    orderinfo = Order.objects.get(code=ordercode)
    print("orderinfo:",orderinfo)
    # print("SQL Query:",orderinfo.query)
    order_product = OrderProduct.objects.filter(user_id=current_user,order__code=ordercode).order_by('id')
    #dateinvoice=datetime.now()
    setting=Setting.objects.get(pk=1)

    context={
           
            'ordercode': ordercode, # old code
            'setting':setting,
            'order_product':order_product,
            #'dateinvoice':dateinvoice,
            'orderinfo': orderinfo,
    }

    return render(request,'print_receipt.html',context)

def invoiceprint_sess(request,ordercode):
    current_user = int(4)
    orderinfo = Order.objects.get(code=ordercode)
    print("orderinfo:",orderinfo)
    # print("SQL Query:",orderinfo.query)
    order_product = OrderProduct.objects.filter(user_id=current_user,order__code=ordercode).order_by('id')
    #dateinvoice=datetime.now()
    setting=Setting.objects.get(pk=1)
    payment=Paymentlist.objects.get(pk=1)
    print(payment)

    context={
           
            'ordercode': ordercode, # old code
            'setting':setting,
            'order_product':order_product,
            'payment':payment,
            'orderinfo': orderinfo,
    }

    return render(request,'invoice_print.html',context)