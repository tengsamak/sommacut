import decimal
import tempfile
from datetime import datetime


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect,get_object_or_404
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
from django_simple_coupons.validations import validate_coupon,Coupon,CouponUser

from .models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from products.models import Product, Category, Variants

from user.models import UserProfile

from home.models import Setting




from django_simple_coupons.models import Coupon



from coupons.form import CouponApplyForm


def index(request):
    return HttpResponse('order page')

# test link*******
def addtoshopcart__t(request,id):
    return HttpResponse(str(id))

@login_required(login_url='/login') # Check login
def addtoshopcart(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product = Product.objects.get(pk=id)

    if product.variant != 'None':    #mean that have Variants
        variantid = request.POST.get('variantid')  # from variant add to cart
        checkinvariant = ShopCart.objects.filter(variant_id=variantid,user_id=current_user.id)  # Check product in shopcart
        if checkinvariant:
            control = 1  # The product is in the cart
        else:
            control = 0  # The product is not in the cart"""
    else:   # mean NO Variant
        checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id)  # Check product in shopcart
        if checkinproduct:
            control = 1  # The product is in the cart
        else:
            control = 0  # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart
                if product.variant == 'None':
                    data = ShopCart.objects.get(product_id=id, user_id=current_user.id)

                else:
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
                #      data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)
                    data.product_id = id
                    data.variant_id = variantid
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
        return HttpResponseRedirect(url)
    #click from index by herf a tag HTML
    else:  # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()  #
        else:  # Inser to Shopcart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.variant_id = None
            data.save()  #
        messages.success(request, "Product added to Shopcart by from Home/index/search page!")
        messages.warning(request,'Click on ShopCart Icon for your oder..')
        return HttpResponseRedirect(url)


@login_required(login_url='/login')
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0


    # count_item=0 # for count items in Cart

    # for rs in shopcart:
    #     total += rs.product.price * rs.quantity
    #     count_item=count_item+1

    # this copy from youtube comment videos
    for rs in shopcart:

        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity
    # return HttpResponse(str(total))
    vat10= total * decimal.Decimal(0.10) # convert float to decimal
    grandtotal=total + vat10


    coupon_apply_form = CouponApplyForm()


    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'vat10': vat10,
               'grandtotal':grandtotal,
               'coupon_apply_form':coupon_apply_form,


               }
    return render(request, 'shopcart_products.html', context)



@login_required(login_url='/login')  # Check login
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted form Shopcart.")
    return HttpResponseRedirect("/shopcart")


def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity
    vat10 = total * decimal.Decimal(0.10)  # convert float to decimal
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
          #  ShopCart.objects.filter(user_id=current_user.id).delete()  # Clear & Delete shopcart
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


class UseCouponView(View):
    def get(self, request, *args, **kwargs):
        coupon_code = request.GET.get("coupon_code")
        user = User.objects.get(username=request.user.username)

        status = validate_coupon(coupon_code=coupon_code, user=user)
        if status['valid']:
            coupon = Coupon.objects.get(code=coupon_code)
            coupon.use_coupon(user=user)

            return HttpResponse("OK")

        return HttpResponse(status['message'])


#for print pdf weasyprint
@staff_member_required
def admin_order_pdf(request,order_id):
	order = get_object_or_404(Order,id=order_id)
	html = render_to_string('pdf.html',{'order':order})
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.id)
	weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
	return response

#for PDF invoice preview
#@login_required(login_url='/login')  # Check login
def generate_pdf(request,ordercode):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    """Generate pdf."""
    # Model data
    orderinfo=Order.objects.filter(user_id=current_user.id,code=ordercode)


    order_product = OrderProduct.objects.filter(user_id=current_user.id,order__code=ordercode)

    context={'orderinfo': orderinfo,
             'setting':setting,
             'ordercode':ordercode,
             'order_product':order_product,
             }
    # Rendered
    html_string = render_to_string('invoice.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(orderinfo)
    weasyprint.HTML(string=html_string,base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response



    # html = weasyprint.HTML(string=html_string)
    # result = html.write_pdf()

    # Creating http response
    # response = HttpResponse(content_type='application/pdf;')
    # response['Content-Disposition'] = 'inline; filename=list_invoice.pdf'
    # response['Content-Transfer-Encoding'] = 'binary'
    # with tempfile.NamedTemporaryFile(delete=True) as output:
    #     output.write(result)
    #     output.flush()
    #     output = open(output.name,'r')
    #     response.write(output.read())
    #
    # return response

