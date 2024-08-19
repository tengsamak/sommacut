from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from vendors.models import Vendor,CommentForm_v,Comment_v

from products.models import Category
from vendors.forms import VendorUserUpdateForm, VendorProfileUpdateForm
from products.models import Product

from django.contrib.auth.models import User
from user.models import UserProfile

from products.models import Images,Comment

from products.models import Variants

from products.models import Color, Size

from order.models import OrderProduct

from order.models import Order
import pandas as pd


def vendorsapp(request):
    vendorslist= Vendor.objects.all()
    context = {'vendorslist': vendorslist,
                }
    return render(request,'test.html',context)

@login_required(login_url='/login') # Check login
def vendor_update(request):
    if request.method == 'POST':
        vendor_user_form = VendorUserUpdateForm(request.POST, instance=request.user)  # request.user is user  data
        vendor_profile_form = VendorProfileUpdateForm(request.POST, request.FILES, instance=request.user.vendor)
        if vendor_user_form.is_valid() and vendor_profile_form.is_valid():
            vendor_user_form.save()
            vendor_profile_form.save()
            messages.success(request, 'Your vendor account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        vendor_user_form = VendorUserUpdateForm(instance=request.user)
        vendor_profile_form = VendorProfileUpdateForm(instance=request.user.vendor)  # "vendoruserprofile" model -> OneToOneField relatinon with user
        context = {
            'category': category,
            'vendor_user_form': vendor_user_form,
            'vendor_profile_form': vendor_profile_form
        }
        return render(request, 'vendor_user_update.html', context)

@login_required(login_url='/login') # Check login
def vendorproductlist(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    vendoractive=User.objects.get(id=current_user.id)

    vendorvendor=Vendor.objects.get(user_id=vendoractive)

    productlist=Product.objects.filter(vendor_id=vendorvendor)
    productlistcount = Product.objects.filter(vendor_id=vendorvendor).count()

    # for test
   # for pl in productlist:
    #    cateproid=Category.objects.filter(id=pl.category_id)

    context = {'category': category,
               'productlist': productlist,
               'productlistcount': productlistcount,

            }
    return render(request, 'vendor_product_list.html', context)


@login_required(login_url='/login') # Check login
def vendorproductdetail(request,pid):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    vendoractive = User.objects.get(id=current_user.id)

    vendorvendor = Vendor.objects.get(user_id=vendoractive)

    productlist = Product.objects.filter(vendor_id=vendorvendor.id,id=pid)
    productimage=Images.objects.filter(product_id=pid)
    productvariant=Variants.objects.filter(product_id=pid)
    productcomments=Comment.objects.filter(product_id=pid)
   # productsize=Size.objects.all()
   # productcolor=Color.objects.all()
    context = {'category': category,
               'productlist': productlist,
              # 'vendorvendor': vendorvendor,
               'productimage':productimage,
               'productvariant':productvariant,
               'productcomments': productcomments,
            #   'productsize':productsize,
            #   'productcolor':productcolor,


               }

    return render(request, 'vendor_product_detail.html', context)

@login_required(login_url='/login') # Check login
def vendorproductorder(request,pid):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    vendoractive = User.objects.get(id=current_user.id)

    vendorvendor = Vendor.objects.get(user_id=vendoractive)

    productlist = Product.objects.filter(vendor_id=vendorvendor.id, id=pid)
    productimage = Images.objects.filter(product_id=pid)
    productvariant = Variants.objects.filter(product_id=pid)
   # productsize = Size.objects.all()
   # productcolor = Color.objects.all()
    product_orderproduct=OrderProduct.objects.filter(product_id=pid).order_by('-create_at')


    #product_orderorder=Order.objects.filter()
    #print("OrderOrder")
    #print(product_orderorder)
    #Join all tables tests
    #orderproducttest1=Order.objects.raw('SELECT * from order_order JOIN order_orderproduct on order_order.id=order_orderproduct.order_id JOIN products_product on order_orderproduct.product_id=products_product.id JOIN vendors_vendor on products_product.vendor_id=vendors_vendor.id ')
   # print(orderproducttest1)
    context = {'category': category,
               'productlist': productlist,
              # 'vendorvendor': vendorvendor,
               'productimage': productimage,
               'productvariant': productvariant,
              # 'productsize': productsize,
              # 'productcolor': productcolor,
               'product_orderproduct' : product_orderproduct,
               #'product_orderorder': product_orderorder,
              # 'orderproducttest1': orderproducttest1,

               }
    return render(request, 'vendor_product_order.html', context)
    #return render(request,'test.html',context)

@login_required(login_url='/login') # Check login
def vendorproductinvoice(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    vendoractive = User.objects.get(id=current_user.id)
    #print(vendoractive) sommachan
    vendorvendor = Vendor.objects.get(user_id=vendoractive)

   # print(vendorvendor) somma group


    productlist = Product.objects.filter(vendor_id=vendorvendor.id)
    userorderproducts=OrderProduct.objects.all()
    userordercodeinvoice=Order.objects.all().order_by('-create_at')

    alluser = User.objects.all()

   # Test for
    totalluserorder=0
    totalordercode=0
    for i in productlist:
       for j in userorderproducts:
          if i.id == j.product_id:
            for k in userordercodeinvoice:
                 if k.id == j.order_id:
                     totalordercode = totalordercode+1
                     totalluserorder = totalluserorder + 1
                        


    print("total user order",totalluserorder)

    print("total code order",totalordercode)



    context = {'category': category,
               'productlist': productlist,
               'userorderproducts': userorderproducts,
               'userordercodeinvoice': userordercodeinvoice,
               'totalordercode': totalordercode,



               }
    return render(request, 'vendor_product_invoice_code_list.html', context)

@login_required(login_url='/login') # Check login
def vendorstatistic(request):
    current_user = request.user  # Access User Session information
    vendoractive = User.objects.get(id=current_user.id)

    vendorvendor = Vendor.objects.get(user_id=vendoractive)

    productlist = Product.objects.filter(vendor_id=vendorvendor)
    #test pandas
    from django_pandas.io import read_frame
    userorderproducts1 = User.objects.values('id','password','username')
    df = pd.DataFrame(userorderproducts1).to_html(index=False)


    productlistcount = Product.objects.filter(vendor_id=vendorvendor).count()
    userorderproducts = OrderProduct.objects.all()
    userordercodeinvoice = Order.objects.all().order_by('-create_at')

    # test pandas
    useridinvoice=Order.objects.values('user_id')
    count=pd.Series(useridinvoice).value_counts()
    print("User_id     Count")
    #print(count)


    alluser=User.objects.all()
    # Test for
    totalluserorder= 0
    totalordercode = 0
    buyerinvoice = []
    for i in productlist:
        for j in userorderproducts:
            if i.id == j.product_id:

                for k in userordercodeinvoice:
                    if k.id == j.order_id:
                        buyerinvoice.append(k.user_id)
                        totalordercode = totalordercode + 1
                        for l in alluser:
                            if l.id ==k.user_id:
                                '''count=pd.Series(alluser).value_counts()
                                print("User     Count")
                                print(count)'''
                                totalluserorder = totalluserorder + 1

   # print(buyerinvoice)
    count1 = pd.Series(buyerinvoice).value_counts() #count value in list by using dataframe pandas to display
    df2=pd.DataFrame(count1)
    df3 = pd.DataFrame(count1)
    print("User     Count1")
    print(count1)

    print(dict((l,buyerinvoice.count(l)) for l in set(buyerinvoice))) # count value in dict
    count2=dict((l,buyerinvoice.count(l)) for l in set(buyerinvoice))
    # to to show username with manytimes to order
    print("useing dictionary")
    for i in count2:
        for j in alluser:
            if j.id == i :
                print("\n",j.username,count2[i])
       # print("% s % d" % (i, count2[i]))
    # test to show all code invoice to user
    #print("code in voice")
    #for i in count2:
    #    for j in userordercodeinvoice:
    #        if j.user_id == i :
    #            print("\n",j.code,i)




    count3=count2.values()
    count4=count2.items()

    context = {'productlistcount': productlistcount,
               'userorderproducts': userorderproducts,
               'userordercodeinvoice': userordercodeinvoice,
               'totalordercode': totalordercode,
               'totalluserorder': totalluserorder,
               'df': df,
               'df2': df2.to_html,
               'df3': df3.to_string(),
               'count2' : count2,
               'count3': count3,
               'count4': count4,
               'alluser': alluser,




               }
    return render(request, 'vendor_summary_statistic_bar.html', context)


@login_required(login_url='/login') # Check login
def vendorstatisticlistinvoicebyid(request,uid):
    current_user = request.user  # Access User Session information
    vendoractive = User.objects.get(id=current_user.id)

    vendorvendor = Vendor.objects.get(user_id=vendoractive)

    productlist = Product.objects.filter(vendor_id=vendorvendor)
    productlistcount = Product.objects.filter(vendor_id=vendorvendor).count()
    userorderproducts = OrderProduct.objects.all()
    userordercodeinvoice = Order.objects.filter(user_id=uid)
    k=0
    stt=[]
    import pandas as pd
    for i in userorderproducts:
        for j in userordercodeinvoice:
            if j.id == i.order_id :
                for l in productlist :
                    if l.id == i.product_id:

                        k=k+1
                        stt.append(j.code)
                        stt.append(j.first_name)

                        print("\n", k)
                        print(j.code)


    context = {'productlistcount': productlistcount,
               'userorderproducts': userorderproducts,
               'userordercodeinvoice': userordercodeinvoice,
               'productlist': productlist,
               'stt': stt,



               }
    return render(request, 'vendor_summary_statistic_bar_by_user_ordercode.html', context)

from home.my_recaptcha import FormWithCaptcha
#add comment to vendor on product and services
def addcomment_v(request,vid):
    url=request.META.get('HTTP_REFERER') #CHECK the last url to return the same page
    #return HttpResponse(url)
    if request.method == 'POST':# check post
        form = CommentForm_v(request.POST)
        captcha=FormWithCaptcha(request.POST)
        if form.is_valid() and captcha.is_valid():
            data = Comment_v()  # create relation with model
            data.subject_v = form.cleaned_data['subject_v']
            data.rate_v = form.cleaned_data['rate_v']     #add get for select
            data.comment_v = form.cleaned_data['comment_v']
            data.ip = request.META.get('REMOTE_ADDR')
            data.vendor_id = vid
            current_user = request.user
            data.user_id = current_user.id
            data.save()  # save data to table
            print("Your review has ben sent. Thank you for your interest")
            messages.success(request, "Your review has ben sent. Thank you for your interest.")
            return HttpResponseRedirect(url)
        else:
            for key, error in list(captcha.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA ")
                    continue
                messages.error(request,error)
    captcha=FormWithCaptcha()
    return HttpResponseRedirect(url)

# def add_follower(request):
#     if request.is_ajax:
#         user_id=int(request.GET['userid'])
#         userfollow=Vendor.objects.get(user_id=user_id)
        
#         print("User id:",user_id)
        
#     return None