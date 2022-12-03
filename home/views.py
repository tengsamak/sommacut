import json

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import translation

from .forms import SearchForm
from .models import Setting, ContactForm, ContactMessage
from products.models import Category, Product, Images,Comment, Variants

# Create your views here.



def home(request):
   # return render(request,'index.html')
    setting= Setting.objects.get(pk=1)
    category=Category.objects.all()
    images= Images.objects.all()
    products=Product.objects.all()
    products_slider=Product.objects.all().order_by('id')[:3] # slide for the first 3 products
    products_latest = Product.objects.all().order_by('-id')[:3] # last 3 products
    products_topsale = Product.objects.all().order_by('?')[:3] # with pick random 3 products
    variants = Variants.objects.all()
    context={'setting':setting,
             'category':category,
             'products_slider':products_slider,
             'products_latest': products_latest,
             'products_topsale': products_topsale,
             'images':images,
             'variants':variants,
             'products':products,
                 }

# copy from product_detail
    # query = request.GET.get('q')
    # if product.variant != "None":  # Product have variants
    #        if request.method == 'POST':  # if we select color
    #         variant_id = request.POST.get('variantid')
    #         variant = Variants.objects.get(id=variant_id)  # selected product by click color radio
    #         colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
    #         sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id', [id])
    #         query += variant.title + ' Size:' + str(variant.size) + ' Color:' + str(variant.color)
    #     else:
    #         variants = Variants.objects.filter(product_id=id)
    #         colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id)
    #         sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id', [id])
    #         variant = Variants.objects.get(id=variants[0].id)
    #    context.update({'sizes': sizes, 'colors': colors,
    #                    'variant': variant, 'query': query
    return render(request,'index.html',context)

def about(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,'category':category
               }
    return render(request,'about.html',context)

def contactus(request):
    category = Category.objects.all()
    if request.method =='POST':  #check the post contact form
        form=ContactForm(request.POST)
        if form.is_valid():
            data=ContactMessage() # create relation with ContactMessage model class
            data.name=form.cleaned_data['name'] #get data form from input data
            data.email=form.cleaned_data['email']
            data.subject=form.cleaned_data['subject']
            data.message=form.cleaned_data['message']
            data.ip=request.META.get('REMOTE_ADDR')
            data.save() # save data to table class model
            messages.success(request,'Your message has been sent, Thank you for your maessage.')
            return HttpResponseRedirect('/contactus')


    setting = Setting.objects.get(pk=1)
    form=ContactForm # sent the form class to pass the html
    context = {'setting': setting,'form':form,'category':category
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

def search(request):
    if request.method=='POST' : # check post
        form=SearchForm(request.POST)
        if form.is_valid():
            query=form.cleaned_data['query'] # get form input data
            catid=form.cleaned_data['catid']
            if catid==0:
                products=Product.objects.filter(title__icontains=query) # select * from product where title LIKE '%query%' this "title__icontains"
                #if form sortby valid
                # p_orderbyname=Product.objects.filter(title__icontains=query).order_by('title')
                # p_orderbylowtohightprice=Product.objects.filter(title__icontains=query).order_by('price')
                # p_orderbyhigthtolowprice=Product.objects.filter(title__icontains=query).order_by('-price')
            else:
                products=Product.objects.filter(title__icontains=query,category_id=catid)
                #if form sortby valid
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
            category=Category.objects.all()
            context={'products':products,
                     'query':query,
                     'category':category,
                     'result_count':result_count,
                     'page':page,
                     }
            return render(request,'product_listing_search_result.html',context)
            #return render(request,'search_products.html',context)
    return HttpResponseRedirect('/')

def search_auto(request):
    if request.is_ajax():
      q = request.GET.get('term', '')
      products = Product.objects.filter(title__icontains=q)
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


def product_detail(request,id,slug):
    query = request.GET.get('q')
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    context = {'product': product,      'category': category,
               'images': images,        'comments': comments,
               }
    if product.variant != "None":  # Product have variants
        if request.method == 'POST':  # if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)  # selected product by click color radio
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
            # pleaed check table name in database sql query
            sizes = Variants.objects.raw('SELECT * FROM  products_variants  WHERE product_id=%s GROUP BY size_id', [id])
            query += variant.title + ' Size:' + str(variant.size) + ' Color:' + str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id)
            sizes = Variants.objects.raw('SELECT * FROM  products_variants  WHERE product_id=%s GROUP BY size_id', [id])
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
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
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
