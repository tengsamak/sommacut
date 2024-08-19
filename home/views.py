import json

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.utils import translation

from .forms import SearchForm
from .models import Setting, ContactForm, ContactMessage
from products.models import Category, Product, Images,Comment, Variants, Event_timer
from django.db.models import Q,Min,Max
#from order.models import ShopCart
from .models import slider,banner
from vendors.models import Comment_v
from django.shortcuts import get_object_or_404


# Create your views here.



def home(request):
   # return render(request,'index.html')
    setting= Setting.objects.get(pk=1)
    slider1 = slider.objects.get(id=1)
    slider2 = slider.objects.get(id=2)
    slider3 = slider.objects.get(id=3)
    banners = banner.objects.all()
    #banner2 = banner.objects.get(id=2)
    category=Category.objects.all()
    images= Images.objects.all()
    products=Product.objects.filter(status=True)
    products_slider=Product.objects.all().order_by('id')[:3] # slide for the first 3 products
    products_latest = Product.objects.all().order_by('-id')[:3] # last 3 products
    #products_topsale = Product.objects.filter(status=True).order_by('?')[:3] # with pick random 3 products
    variants = Variants.objects.all() 
    
    #for display unique categories
    setcategory=[]
    for i in products:
        setcategory.append(i.category.title)
    uniquecate=set(setcategory)
    #shopcart=ShopCart.objects.all()
    context={'setting':setting,
            'category':category,
            'products_slider':products_slider,
            'products_latest': products_latest,
            # 'products_topsale': products_topsale,
            'images':images,
            'variants':variants,
            'products':products,
            #  'shopcart':shopcart,
            'uniquecate':uniquecate,
            'slider1':slider1,
            'slider2':slider2,
            'slider3':slider3,
            'banners':banners,
            #'banner2':banner2,
            
            
            }

    return render(request,'index.html',context)

def about(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,'category':category
               }
    return render(request,'about.html',context)

def termofservices(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,'category':category
               }
    return render(request,'termofservice.html',context)

def privacypolicy(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,'category':category
               }
    return render(request,'privacypolicy.html',context)

def buyingguide(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,'category':category
               }
    return render(request,'buyingguide.html',context)

from django.core.mail import send_mail
from django.conf import settings
from .my_recaptcha import FormWithCaptcha
def contactus(request):
    
    if request.method =='POST':  #check the post contact form
        contactname=request.POST['contact_name'] #get data form from input data
        contactemail=request.POST['contact_email']
        contactmessage=request.POST['contact_message']
        #email_from = settings.EMAIL_HOST_USER
        data={
            'name':contactname,
            'email':contactemail,
            'message':contactmessage,
        }
        messsage =''' 
        New message from SOMMASTORE:
        Subject:{}
        Message:{}
        Email-From:{}
        '''.format(data['name'],data['message'],data['email'])
        send_mail(data['name'],messsage,'', ['tengsamak@gmail.com'])
        #return render(request, 'success.html') 
        #print(contactname,contactemail,contactmessage)
        
        return HttpResponseRedirect('/contactus')

    setting = Setting.objects.get(pk=1)
    #form=ContactForm # sent the form class to pass the html
    context = {'setting': setting,
               'captcha':FormWithCaptcha,
              
               }
    return render(request,'contactus.html',context)


def category_products(request,id,slug):
    # setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    context = {
           'products': products,
           'category': category,
                      }
    return render(request,'category_products.html',context)
   # return HttpResponse(products) # test link products

#old search fucntion with forms.py
def search(request):
    if request.method=='POST' : # check post
        form=SearchForm(request.POST)
        if form.is_valid():
            query=form.cleaned_data['query'] # get form input data
            catid=form.cleaned_data['catid']
            
            print("#######your query:",query)
            print("#######your category ID:",catid)
            if catid==63:
            #if catid=="0" and query=="" :
                #products=Product.objects.filter(title__icontains=query)
                products=Product.objects.all()
            elif query== str(""):
                procatelist=Product.objects.select_related('Category').get(parent_id=catid)#Inner Join two tabless
                for rs in procatelist:
                    print("######## Products List #######")
                    print(rs.title)
                    print("###end###")
                pass
            #     products=Product.objects.filter(title__icontains=query)
            else:
                products=Product.objects.filter(title__icontains=query)
                #products=Product.objects.filter(title__icontains=query,category_id=catid)
            catname=Category.objects.filter(id=catid)
            #catelist=Category.objects.fiter(parent_id=catid)
            category = Category.objects.all()
            #products=Product.objects.filter(Q(title__icontains=query) | Q(category_id=catid))
                #if form sortby valid
            # ****paginator
            # product_paginator = Paginator(products, 25)  # 25 products per page
            # page_num = request.GET.get('page')  # get page number
            # try:
            #     page = product_paginator.page(page_num)
            # except PageNotAnInteger:
            #     page = product_paginator.page(1)
            # except EmptyPage:
            #     page= product_paginator.page(product_paginator.num_pages)
            # result_count = product_paginator.count
                # *************
            #print(category,"allcate")
            context={'products':products,
                     'query':query,
                     'catid':catid,
                     'catname':catname,
                     'category':category,
                    # 'catelist':catelist, # get parent_id to get catid for product id list
                    # 'procatelist':procatelist,
                    #  'result_count':result_count,
                    #  'page':page,
                     }
            return render(request,'product_listing_search_result.html',context)
  
    #return HttpResponse("home")    
    return HttpResponseRedirect('/')
    
# now we use this function test for Html form    
def searchbar_(request):
    
    error=False # កុងតាត់ to check
    if request.POST:
        #check one by one input form
        # if 'catid'==0 and 'query'=="" in request.POST:
        #         return HttpResponseRedirect('/')
        # else:
        #     error=True
        #     messages.info(request,"Error")
        if 'catid' in request.POST:
            catid=request.POST.get('catid','')
            print("###### The category is:",catid)
            print("print products related with categorie")
            products=Product.objects.filter(category_id=catid)
            print(products)
            #procatelist=Product.objects.select_related('Category').get(parent_id=catid)#Inner Join two tabless
            #procatelist=Product.objects.raw("SELECT * FROM products_product inner join products_category on (products_product.category_id=products_category.id)where products_category.parent_id=catid")
            
            
        else:
            error=True
            messages.info(request,"Please Choose Category of product")
        if 'query' in request.POST:
            query=request.POST.get('query','')
            print("##########the query is: ",str(query))
            products=Product.objects.filter(title__icontains=query)
       
        else:
            error=True
            messages.info(request,"Please Input Product's Name")
        if not error:
            # if 'catid'==0 and 'query'=="":
            #     return HttpResponseRedirect('/')
            # messages.info(request,"product and cate")
           
            #categoryname=Category.objects.filter(id=catid)
           # category = Category.objects.filter(id=catid)
            #products=Product.objects.filter(title__icontains=query)
            products=Product.objects.filter(Q(title__icontains=query) | Q(category_id=catid))
            print("*********************************")
            print(products)
             # ****paginator
            # product_paginator = Paginator(products, 25)  # 25 products per page
            # page_num = request.GET.get('page')  # get page number
            # try:
            #     page = product_paginator.page(page_num)
            # except PageNotAnInteger:
            #     page = product_paginator.page(1)
            # except EmptyPage:
            #     page= product_paginator.page(product_paginator.num_pages)
            # result_count = product_paginator.count
                # *************
            # we show this input to table sucess
        catname=Category.objects.filter(id=catid)
        category = Category.objects.all()    
        context={
                'products':products,
                'catname':catname,
               # 'categoryname':categoryname,
                'category':category,
                'catid':catid,
                'query':query,
              #  'result_count':result_count,
              #  'page':page,
                
            }
        return render(request,'product_listing_search_result.html',context)
   
    else:
           # if 'catid'==0 and 'query'=="":
        return HttpResponseRedirect('/')
    
def searchbar(request):
    # error=False # កុងតាត់ to check
    #url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        
        query=request.POST['query']
        searchpro=Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) |Q(title_kh__icontains=query),status=True)
        #searchpro=Product.objects.filter(Q(title__icontains=query) and Q(status=True))
        #searchpro=Product.objects.filter(title__icontains=query, status=True)
        #for category list
        setcategory=[]
        for i in searchpro:
            setcategory.append(i.category.title)
        uniquecate=set(setcategory)
        #End for category list
        if not query or searchpro.count() == 0 :
            searchproall=Product.objects.filter(status=True)
            context={
                'products':searchproall,
                'query':query,
                'uniquecate':uniquecate,
                
            }
            messages.info(request,"That Product does not existed ")
            return render(request,'product_listing_search_result.html',context)
            #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            context={
                'products':searchpro,
                'query':query,
                'uniquecate':uniquecate,
                
            }
            return render(request,'product_listing_search_result.html',context)
    else:
        messages.info(request,"Please search your products... ")
        #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect('/')    
        
        
def search_auto(request):
    if request.is_ajax():
      q = request.GET.get('term', '')
      products = Product.objects.filter(Q(title__icontains=q) and Q(status=True))
      results = []
      for rs in products:
        product_json = {}
        product_json = rs.title
        results.append(product_json)
      data = json.dumps(results)
    else:
      data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

#search product in vendor by title auto
def provensearch_auto(request,vid):
    if request.is_ajax():
        #vid=request.GET.get('v_id')
        q=request.GET.get('term','')
        products=Product.objects.filter(vendor_id=vid,status=True,title__icontains=q)
        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

#after search auto product in vendor will request ajax for query product
def provensearchajax(request):
    data = {}
    vid=int(request.POST.get('vendorid'))
    #vid=request.POST.get('vendorid')
    print(type(vid))
    #if request.POST.get('action') == 'post':
    #if request.POST:
        #if 'query' or  in request.POST:
        #query=request.POST.get('query','')
        #vid=request.POST.get('vendorid','')
        #vid=int(request.POST.get('vid'))
        #print("in First query",query)
        #print("in First vid:",vid)
    print("out First vid",vid)
    products=Product.objects.filter(vendor_id=vid,status=True)
    productscount=Product.objects.values('vendor_id').annotate(count=Count('vendor_id')).filter(status=True,vendor_id=vid)
    images= Images.objects.all()
    vendorinfo=Vendor.objects.get(pk=vid)
    # ****paginator
    '''
    
    product_paginator = Paginator(products, 20)  # 20 products per page
    page_num = request.GET.get('page')  # get page number
    try:
        page = product_paginator.page(page_num)
    except PageNotAnInteger:
        page = product_paginator.page(1)
    except EmptyPage:
        page= product_paginator.page(product_paginator.num_pages)
    result_count = product_paginator.count
    '''
        # *************    
    for i in productscount:
        for j in products:        
            if j.vendor_id == i['vendor_id'] :
                productscount=int(i['count'])
            else:
                productscount=0
    context = {
        
        #'result_count':result_count,
        #'page':page,
        #'categoryname':categoryname,
        'images':images,
        'vendorinfo':vendorinfo,
        'productscount':productscount,
        
        }
    #print(productscount[0])
    
    #if request.POST.get('action') == 'post':
    if request.POST:
        if 'query' in request.POST:
            query=request.POST.get('query','')
            #vid=request.POST.get('vendorid')
            vid=int(request.POST.get('vendorid'))
            print("second vid",vid)
            
            print("##########the query is: ",str(query))
            ajaxproducts=Product.objects.filter(vendor_id=vid,status=True,title__icontains=query)
            print("this is ajaxproduct:",ajaxproducts)
            context.update({
            'ajaxproducts':ajaxproducts,
            })
            
            data = {'rendered_table': render_to_string('ajaxprovensearch_test.html', context=context)}
            print("data query",data)
            return JsonResponse(data)
            
        else:
            return HttpResponseBadRequest('Invalid request')
            #error=True
            #messages.info(request,"Please Input Product's Name")
            
        
    
        messages.info(request,"Please fell free to inform us something errors!")
    #categoryname=Category.objects.filter(id=cid)
    return JsonResponse(data)

def provensearchajax_test(request):
    data = {} 
    if request.POST:
        if 'query' in request.POST:
    # data = {}
    # if request.POST.get('action') == 'post':
            query=request.POST.get('query')
            #vid=request.POST.get('vendorid')
            vid=int(request.POST.get('vendorid'))
            print("second vid",vid)
            
            print("##########the query is: ",str(query))
            context={
                'query':query,
                'vid':vid,
                
            }
            data = {'rendered_table': render_to_string('ajaxprovensearch_test.html', context=context)}
            print("data query",data)
            return JsonResponse(data)
            
        else:
            return HttpResponseBadRequest('Invalid request')
    return HttpResponseBadRequest('Invalid request')

#search product without Ajax
def provensearch(request,vid):
    products=Product.objects.filter(vendor_id=vid,status=True).order_by('title')
    productscount=Product.objects.values('vendor_id').annotate(count=Count('vendor_id')).filter(status=True,vendor_id=vid)
    
    #print(productscount[0])
    for i in productscount:
        for j in products:        
            if j.vendor_id == i['vendor_id'] :
                productscount=int(i['count'])
            else:
                productscount=0
    #if request.POST.get('action') == 'post':
    if request.POST:
        if 'query' in request.POST:
            query=request.POST.get('query','')
            print("##########the query is: ",str(query))
            products=Product.objects.filter(vendor_id=vid,status=True,title__icontains=query)
       
        else:
            #error=True
            messages.info(request,"Please Input Product's Name")
        
    else:
        messages.info(request,"Please fell free to inform us something errors!")
    #categoryname=Category.objects.filter(id=cid)
    images= Images.objects.all()
    vendorinfo=Vendor.objects.get(pk=vid)
    context = {
        'products':products,
        #'result_count':result_count,
        #'page':page,
        #'categoryname':categoryname,
        'images':images,
        'vendorinfo':vendorinfo,
        'productscount':productscount,
        #'products_order_name':products_order_name,
        'vid':vid,
        }
    
    return 
   
        

from vendors.models import CommentForm_v
def product_detail(request,id,slug):
    query = request.GET.get('q')
    category = Category.objects.all()
    product = Product.objects.get(pk=id,status=True)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    comments_v = Comment_v.objects.filter(vendor=product.vendor_id, status='True')
    #products_topsale = Product.objects.all().order_by('?')[:3] # with pick random 3 products
    #related_products = Product.objects.filter(category_id=product.category_id,status=True).exclude(id=id)#related product get in the category
    related_products = Product.objects.filter(status=True).exclude(id=id)[:5]#related product get in the category
    product_list_by_vendor = Product.objects.filter(vendor_id=product.vendor_id,status=True) # show as relative products
    #product_list_by_vendor_count=product_list_by_vendor = Product.objects.filter(vendor_id=product.vendor_id,status=True).count()
    product_list_by_vendor_count = Product.objects.filter(vendor_id=product.vendor_id,status=True).count()
    #product_list_by_vendor_count=Product.objects.values('vendor_id').annotate(count=Count('vendor_id'))
    # count products by vendor_id
    #pro_count_by_vendor=Product.objects.values('vendor_id').annotate(count=Count('vendor_id')).filter(status=True)
    # for j in pro_count_by_vendor:
    #     if product.vendor_id == j['vendor_id']:
    #         #print(j['count'])
    #         vendorprocount=int(j['count'])
    
    context = {'product': product,      'category': category,
               'images': images,        'comments': comments,
               
               'comments_v':comments_v,
               #'products_topsale':products_topsale,
               'related_products':related_products,
               'product_list_by_vendor':product_list_by_vendor,
               'product_list_by_vendor_count':product_list_by_vendor_count,
               'captcha':FormWithCaptcha,
               'form' : CommentForm_v(),
               }
    if product.variant != "None":  # Product have variants
        if request.method == 'POST':  # if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)  # selected product by click color radio
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id).order_by('-quantity')
            # pleaed check table name in database sql query
            #sizes = Variants.objects.raw('SELECT * FROM  products_variants  WHERE product_id=%s GROUP BY size_id', [id])
            sizes = Variants.objects.raw('SELECT * FROM  products_variants  WHERE product_id=%s GROUP BY size_id ORDER BY quantity DESC', [id])
            query += variant.title + ' Size:' + str(variant.size) + ' Color:' + str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id).order_by('-quantity')
            colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id).order_by('-quantity')
            #sizes = Variants.objects.raw('SELECT * FROM  products_variants  WHERE product_id=%s GROUP BY size_id', [id])
            sizes = Variants.objects.raw('SELECT * FROM  products_variants  WHERE product_id=%s GROUP BY size_id ORDER BY quantity DESC', [id])
            variant = Variants.objects.get(id=variants[0].id)
        context.update({'sizes': sizes,         'colors': colors,
                        'variant': variant,     'query': query
                        })
    
    return render(request, 'product_detail.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id).order_by('-quantity')
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)

def selectedpro(request):
    data={}
    if request.POST.get('action') == 'post':
        proid=request.POST.get('proid')
        sizeid=request.POST.get('sizeid')
        colorid=request.POST.get('colorid')
        productid=Product.objects.filter(id=proid)
        qty= request.POST.get('qty')
        #print("quantity:",qty)
        
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
                variant=Variants.objects.get(id=variantid)
                context={
                    'proid':proid,
                    'varinatname':sizeid,
                    'variantcolor':variantcolor,
                    'variantid':variantid,
                    'variant':variant,
                    'qty':qty  , 
                             
                    }
        elif sizeid=='Size':
                
                variantid=j[0]
                variantsize=j[1]
                print("***Size****")   
                print("VariantID:",variantid) 
                print("SizeID:",variantsize) 
                print("***********")
                variant=Variants.objects.get(id=variantid)
                context={
                    'proid':proid,
                    'varinatname':sizeid,
                    'variantsize':variantsize,
                    'variantid':variantid,
                    'variant':variant,
                    'qty':qty  ,          
                    }
        else:
                variantid=j[0]
                variantsize=j[1]
                variantcolor=j[2]
                print("****Size and Color***")   
                print(variantid) 
                print(variantsize)
                print(variantcolor)     
                print("***********")
                variant=Variants.objects.get(id=variantid)
                context={
                    'proid':proid,
                    'varinatname':sizeid,
                    'variantid':variantid,
                    'variantsize':variantsize,
                    'variantcolor':variantcolor,
                    'variant':variant, 
                    'qty':qty  ,      
                    }
                
                     
                
        #for x in l:
        #    print(x)
        
        
        getcontex=context
        # context={
        #     'proid':proid,
        #     'sizeid':sizeid,
        #     'colorid':colorid,
        #     'variant':variant,         
        # }
        print("Print context selected data")
        print(getcontex)
        #check login and session for not login
        if request.user.is_authenticated:
            data={'rendered_table':render_to_string('selectedpro.html',context=getcontex)}
        else: 
            data={'rendered_table':render_to_string('selectedpro_sess.html',context=getcontex)}
        return JsonResponse(data)
    return JsonResponse(data)
        
        
        

    # category = Category.objects.all()
    # product = Product.objects.get(pk=id)
    # images=Images.objects.filter(product_id=id)
    # comments = Comment.objects.filter(product_id=id,status='True')
    # context = {
    #     'product': product,
    #     'category': category,
    #     'images':images,
    #     'comments': comments,
    # }
    # return render(request,'product_detail.html',context)

# for multi languages
def selectlanguage(request):
    if request.method == 'POST':  # check post
        cur_language = translation.get_language()
        lasturl= request.META.get('HTTP_REFERER')
        lang = request.POST['language']
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY]=lang
       # return HttpResponse(lang)
        return HttpResponseRedirect("/"+lang)

#search product category at the index by parents_id
def searchcate(request,id):
    if id==63:
        products=Product.objects.filter(status=True)
        parentid=id
    #messages.info(request,"you got in searchcate")
    #products=Product.objects.select_related('Category').get(parent_id=id)#Inner Join two tabless
    else:
        products=Product.objects.raw('SELECT * FROM products_product inner join products_category on (products_product.category_id=products_category.id) where products_product.status="True" AND products_category.parent_id= %s',[id])
        parentid=id
    print(products)
    images= Images.objects.all()
    categoryname=Category.objects.filter(id=id)
    
    #for leftsidebar
    #provenleftsidebar= Product.objects.values('category_id','category__title').annotate(countcate=Count('category_id')).filter(status=True)
    # min_price = Product.objects.all().aggregate(Min('price'))
    # max_price = Product.objects.all().aggregate(Max('price'))
    # print(min_price)
    # print(max_price)
    #print("provenleftsidebar",provenleftsidebar)
    #end leftsidebar
    

        # ****paginator
    product_paginator = Paginator(products, 25)  # 25 products per page
    page_num = request.GET.get('page')  # get page number
    try:
        page = product_paginator.page(page_num)
    except PageNotAnInteger:
        page = product_paginator.page(1)
    except EmptyPage:
        page= product_paginator.page(product_paginator.num_pages)
    result_count = product_paginator.count
        # *************
    context={
        'products':products,
        'images':images,
        'categoryname':categoryname,
        'result_count':result_count, # we used this product count 
        'page':page,
        'parentid':parentid, #cheked id 63 for all
        #forsidebar
        #'provenleftsidebar':provenleftsidebar,
        # 'min_price':min_price,
        # 'max_price':max_price,
        #endsidebar
       
    }
    return render(request,'category_listing_search_result.html',context)
#list products by category_id leftsidebar
def searchprocate(request,cid):
    
    products=Product.objects.filter(status=True,category_id=cid)
    images= Images.objects.all()
    categoryname=Category.objects.filter(id=cid)

        # ****paginator
    product_paginator = Paginator(products, 25)  # 25 products per page
    page_num = request.GET.get('page')  # get page number
    try:
        page = product_paginator.page(page_num)
    except PageNotAnInteger:
        page = product_paginator.page(1)
    except EmptyPage:
        page= product_paginator.page(product_paginator.num_pages)
    result_count = product_paginator.count
        # *************
    #leftsidebar
    
    # procateleftsidebar= Product.objects.values('category_id','category__title').annotate(countcate=Count('category_id')).filter(status=True)
    # min_price = Product.objects.all().aggregate(Min('price'))
    # max_price = Product.objects.all().aggregate(Max('price'))
    #endleftsidebar
    
    context={
        'products':products,
        'images':images,
        'categoryname':categoryname,
        'result_count':result_count, # we used this product count 
        'page':page,
        # 'procateleftsidebar':procateleftsidebar,
        # 'min_price':min_price,
        # 'max_price':max_price,
    }
    return render(request,'category_listing_search_result copy.html',context)    
    
    # search category product at productdetail with category_id and slug
def searchcateid(request,id,slug):
    images= Images.objects.all()
    categoryname=Category.objects.filter(id=id)
    products=Product.objects.raw('SELECT * FROM products_product inner join products_category on (products_product.category_id=products_category.id) where products_product.status="True" AND products_product.category_id= %s',[id])
    
    # ****paginator
    product_paginator = Paginator(products, 25)  # 25 products per page
    page_num = request.GET.get('page')  # get page number
    try:
        page = product_paginator.page(page_num)
    except PageNotAnInteger:
        page = product_paginator.page(1)
    except EmptyPage:
        page= product_paginator.page(product_paginator.num_pages)
    result_count = product_paginator.count
        # *************    
    context={
            'products':products,
            'images':images,
           
            'categoryname':categoryname,
            'result_count':result_count,
            'page':page,
           
        }
        
        
    return render(request,'category_listing_search_result.html',context)

#list vendor detail and products
from vendors.models import Vendor
def searchvendor(request,vid,cid):
    products=Product.objects.filter(vendor_id=vid,status=True).order_by('-title')
    products_order_name=Product.objects.filter(vendor_id=vid,status=True).order_by('title').values()
    #productscount=Product.objects.values('vendor_id').annotate(count=Count('vendor_id')).filter(status=True,vendor_id=vid)
    productscount=Product.objects.filter(vendor_id=vid,status=True).count()
   
    
    categoryname=Category.objects.filter(id=cid)
    images= Images.objects.all()
    vendorinfo=Vendor.objects.get(pk=vid)
    setcategory=[]
    for i in products:
        setcategory.append(i.category.title)
    uniquecate=set(setcategory)
    #for display unique categories
    # setcategory=[]
    # setcategoryid=[]
    # for i in Product.objects.filter(status=True).order_by('-category_id'):
    #     setcategory.append(i.category.title)
    #     #print(i.category.title)
    #     #print(i.id)
    #     setcategoryid.append(i.category.id)
    # uniquecate=set(setcategory)
    # uniquecateid=set(setcategoryid)
    #print(uniquecateid)
    #print(uniquecate)
    
    #for leftsidebar
    # provenleftsidebar= Product.objects.values('category_id','category__title').annotate(countcate=Count('category_id')).filter(status=True)
    # min_price = Product.objects.all().aggregate(Min('price'))
    # max_price = Product.objects.all().aggregate(Max('price'))
    # print(min_price)
    # print(max_price)
    # print("provenleftsidebar",provenleftsidebar)
    #end leftsidebar
    
    # ****paginator
    
    product_paginator = Paginator(products, 1)  # 20 products per page
    page_num = request.GET.get('page',1)  # get page number
    pro_page=product_paginator.get_page(page_num)
    try:
        page = product_paginator.page(page_num)
    except PageNotAnInteger:
        page = product_paginator.page(1)
    except EmptyPage:
        page= product_paginator.page(product_paginator.num_pages)
    result_count = product_paginator.count
    
        # *************    
    context={
        'products':products,
        'result_count':result_count,
        'page':page,
        'pro_page':pro_page,
        'categoryname':categoryname,
        'images':images,
        'vendorinfo':vendorinfo,
        'productscount':productscount,
        'uniquecate':uniquecate,
        # 'uniquecateid':uniquecateid,
        'products_order_name':products_order_name,
        # 'provenleftsidebar':provenleftsidebar,
        'vid':vid,
        # 'min_price':min_price,
        # 'max_price':max_price,
        
        
    }
    return render(request,'vendor_products_listing_search_result.html',context)

# list product from price range filter
#import math
def pricerangefilter(request):
    data={}
    if request.POST.get('action') == 'post':
        getpmin=request.POST.get('pmin')
        getpmax=request.POST.get('pmax')
        print(getpmin.removeprefix('$'))# remove $ sign
        print(getpmax.removeprefix('$'))# remove $ sign
        pmin=float(getpmin.removeprefix('$'))
        pmax=float(getpmax.removeprefix('$'))
        print(pmin)
        print(pmax)
        products=Product.objects.filter(price__range=(pmin, pmax),status=True)
    else:
        products=Product.objects.filter(status=True)        
        
    #categoryname=Category.objects.filter(id=cid)
    images= Images.objects.all()
    #products=Product.objects.filter(status=True)
    # ****paginator
    product_paginator = Paginator(products, 25)  # 25 products per page
    page_num = request.GET.get('page')  # get page number
    try:
        page = product_paginator.page(page_num)
    except PageNotAnInteger:
        page = product_paginator.page(1)
    except EmptyPage:
        page= product_paginator.page(product_paginator.num_pages)
    result_count = product_paginator.count
    
    context={
        'products':products,
        'images':images,
           
        'categoryname':'Filter By Price',
        'result_count':result_count,
        'page':page,
        'pmin':pmin,
        'pmax':pmax,
    }
    data={'rendered_table':render_to_string('ajaxpricerangefilter.html',context=context)}    
    #return render(request,'vendor_products_listing_search_result.html',context=context)
    return JsonResponse(data)

#Ajax function for sort product by vendor
def sortproven(request):
    data={}
    getvalue=int(request.GET['sort_fc'])
    vid=int(request.GET['v_id'])
    cid=int(request.GET['c_id'])
    print(getvalue)
    print(vid)
    print(cid)
    #products_order_name_a_z=Product.objects.filter(vendor_id=vid,status=True).order_by('title').values()
    productscount=Product.objects.values('vendor_id').annotate(count=Count('vendor_id')).filter(status=True,vendor_id=vid)
    if getvalue == 1 : #Name(A-Z)
        products_order=Product.objects.filter(vendor_id=vid,status=True).order_by('title')
    
    if getvalue == 2 : #Name(Z-A)
        products_order=Product.objects.filter(vendor_id=vid,status=True).order_by('-title')
        
    
    if getvalue == 3 : #Price (Low to High)
        products_order=Product.objects.filter(vendor_id=vid,status=True).order_by('price')
        
    if getvalue == 4 : #Price (High to Low)   
        products_order=Product.objects.filter(vendor_id=vid,status=True).order_by('-price')
    
    if getvalue == 0:
        products_order=Product.objects.filter(vendor_id=vid,status=True)
    
    #print(productscount[0])
    products=Product.objects.filter(vendor_id=vid,status=True)
    for i in productscount:
        for j in products:        
            if j.vendor_id == i['vendor_id'] :
                productscount=int(i['count'])
            else:
                productscount=0
        
    categoryname=Category.objects.filter(id=cid)
    images= Images.objects.all()
    # for rs in products_order:
    #     for pr in images:
    #         if rs.id == pr.product_id:
    #             pr.image.url
    vendorinfo=Vendor.objects.get(pk=vid)
    context={
        'categoryname':categoryname,
        'images':images,
        'vendorinfo':vendorinfo,
        'productscount':productscount,
        'products_order':products_order,
    
    }    

    data={'rendered_table':render_to_string('ajaxsortprovendor.html',context=context)}    
    print(data)
    return JsonResponse(data)

# sort by Ajax Category and category_id with parent_id
def sortcate(request):
    data={}
    getvalue=int(request.GET['sort_cate'])
    # vid=int(request.GET['v_id'])
    parentid=int(request.GET['parent_id'])
    print(getvalue,parentid)
    if parentid == 63:
        # parentid = parentid
        if getvalue == 1 : #Name(A-Z) 
            products_order=Product.objects.filter(status=True).order_by('title')
        if getvalue == 2 : #Name(Z-A)
            products_order=Product.objects.filter(status=True).order_by('-title')
        if getvalue == 3 : #Price (Low to High)
            products_order=Product.objects.filter(status=True).order_by('price')
        if getvalue == 4 : #Price (High to Low) 
            products_order=Product.objects.filter(status=True).order_by('-price')
    else:
        # parentid = parentid
    #products=Product.objects.raw('SELECT * FROM products_product inner join products_category on (products_product.category_id=products_category.id) where products_product.status="True" AND products_category.parent_id= %s',[cid])
    #productscount=Product.objects.values('category_id').annotate(count=Count('category_id')).filter(status=True)
        if getvalue == 1 : #Name(A-Z)
            #products_order=Product.objects.filter(Q(category_id=cid,status=True)|Q(category__parent_id=cid,status=True)).order_by('title')
            #products= Product.objects.select_related('category').get(parent_id=cid)
            products_order=Product.objects.raw('SELECT * FROM products_product inner join products_category on (products_product.category_id=products_category.id) where products_product.status="True" AND products_category.parent_id= %s ORDER by title ASC',[parentid])
        if getvalue == 2 : #Name(Z-A)
            #products_order=Product.objects.filter(Q(category_id=cid,status=True)|Q(category__parent_id=cid,status=True)).order_by('-title')
            products_order=Product.objects.raw('SELECT * FROM products_product inner join products_category on (products_product.category_id=products_category.id) where products_product.status="True" AND products_category.parent_id= %s ORDER by title DESC',[parentid])
        if getvalue == 3 : #Price (Low to High)
            #products_order=Product.objects.filter(Q(category_id=cid,status=True)|Q(category__parent_id=cid,status=True)).order_by('price')    
            products_order=Product.objects.raw('SELECT * FROM products_product inner join products_category on (products_product.category_id=products_category.id) where products_product.status="True" AND products_category.parent_id= %s ORDER by price ASC',[parentid])
        if getvalue == 4 : #Price (High to Low)   
            #products_order=Product.objects.filter(Q(category_id=cid,status=True)|Q(category__parent_id=cid,status=True)).order_by('-price')  
            products_order=Product.objects.raw('SELECT * FROM products_product inner join products_category on (products_product.category_id=products_category.id) where products_product.status="True" AND products_category.parent_id= %s ORDER by price DESC',[parentid])
    # print(products_order)
    # categoryname=Product.objects.filter(Q(category_id=parentid,status=True)|Q(category__parent_id=parentid,status=True))
    images= Images.objects.all()
    context={
        # 'categoryname':categoryname,
        'images':images,
        'products_order':products_order,
        'parentid' : parentid,
        # 'sortcate':sortcate,
    }    
    data={'rendered_table':render_to_string('ajaxsortcate.html',context=context)}    
    # print(data)
    return JsonResponse(data)

def sortprocate(request):
    data={}
    getvalue=int(request.GET['sort_procate'])
    # vid=int(request.GET['v_id'])
    cid=int(request.GET['c_id'])
    print(getvalue,cid)
    if getvalue == 1 : #Name(A-Z)
        products_order=Product.objects.filter(status=True,category_id=cid).order_by('title')
    if getvalue == 2 : #Name(Z-A)
        products_order=Product.objects.filter(status=True,category_id=cid).order_by('-title')
    if getvalue == 3 : #Price (Low to High)
        products_order=Product.objects.filter(status=True,category_id=cid).order_by('price')
    if getvalue == 4 : #Price (High to Low) 
        products_order=Product.objects.filter(status=True,category_id=cid).order_by('-price')
        
    context={
        'products_order':products_order,
        # 'sortprocate':sortprocate,
        
    }
    data={'rendered_table':render_to_string('ajaxsortprocate.html',context=context)}    
    print(data)
    return JsonResponse(data)

# List all vendor with related product count and click for vendor detail
from order.models import Order,OrderProduct
from django.db.models import Count       
from django.db.models import Max 
def vendorlist(request):
    vendors=Vendor.objects.filter(status="New")
    products=Product.objects.filter(status=True)
    #pro_count_by_vendor=Product.objects.annotate(count=Count('vendor_id')).values('vendor_id','count').filter(status=True)
    pro_count_by_vendor=Product.objects.values('vendor_id').annotate(count=Count('vendor_id')).filter(status=True)
    #pro_count_by_vendor= Product.objects.raw('SELECT vendor_id,count(vendor_id) as Productcountbyvendor from products_product where status="True" GROUP by vendor_id')
    
    # print(pro_count_by_vendor)
   
    # for i in vendors:
    #     for j in pro_count_by_vendor:
    #         if i.id == j['vendor_id']:
    #             print(j['count'])
                
        
    # ****paginator
    
    product_paginator = Paginator(vendors, 1)  # 20 products per page
    page_num = request.GET.get('page',1)  # get page number
    #pro_page=product_paginator.get_page(page_num)
    try:
        page = product_paginator.page(page_num)
    except PageNotAnInteger:
        page = product_paginator.page(1)
    except EmptyPage:
        page= product_paginator.page(product_paginator.num_pages)
    result_count = product_paginator.count
    
        # *************  
    #Recent products post     
    p_recent_post=Product.objects.filter(status=True).order_by('-update_at')[:3]    
    # Best Seller Produts
    #count_order_p=OrderProduct.objects.values('product_id').annotate(count=Count('product_id')).aggregate(Max('count'))
    count_order_p=OrderProduct.objects.values('product_id').annotate(count=Count('product_id')).order_by('-count')[:3]
    list_p_id=[] # for store product id 
    for i in count_order_p:
        # print("Pro:",i['product_id'])
        list_p_id.append(i['product_id'])
          
    #best sell product
    p_best_seller=Product.objects.filter(id__in=list_p_id)
    # print("count group by Product:",count_order_p)
    # print("best seller:",p_best_seller)
    tags = Tag.objects.all()
    context={
        'page':page,
        'result_count':result_count,
        'vendors':vendors,
        'pro_count_by_vendor':pro_count_by_vendor,
        'products':products,
        # product recen post by update date
        'p_recent_post':p_recent_post,
        #best seller product:
        'p_best_seller':p_best_seller,
        #for list tags
        'tags':tags,
    }
    return render(request,'vendor_listing.html',context)

def vendorsearch_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        vendors = Vendor.objects.filter(companyname__icontains=q)
        results = []
        for rs in vendors:
            vendor_json = {}
            vendor_json = rs.companyname
            results.append(vendor_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
    
    
def product_listing(request):
    
    context={}
    return render(request,'products_listing_test.html',context)

from django.shortcuts import get_object_or_404
from taggit.models import Tag
def pro_filter_tag(request,tagname):
    tag = get_object_or_404(Tag, name=tagname)
    #products=get_object_or_404(Product,tags__icontains=tagname,status=True)
    products = Product.objects.filter(tags=tag)
    #for listing category
    setcategory=[]
    for i in products:
        setcategory.append(i.category.title)
    uniquecate=set(setcategory)
    #end listing
    context={
        'products':products,
        'query':tag,
        'uniquecate':uniquecate,
        
    }
    return render(request,'product_listing_search_result.html',context)




# call function expired_dis_timer Ajax
def expired_dis_timer(request):
    data={}
    pid=int(request.GET['pid_'])
    print(pid)
    pro_price = Product.objects.get(id=pid)
    pro_price.price = pro_price.m_price
    pro_price.save()
    event_status=Event_timer.objects.get(product_id=pid)
    event_status.status="Expired"
    event_status.save()
    content={
        'products':pro_price.price,
    }
    data=content
    print(data)
    
    return JsonResponse(data)
 