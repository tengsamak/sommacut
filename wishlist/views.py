#from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from order.models import ShopCart
# Create your views here.
#def wishlist(request):
#    return HttpResponse('Hello Wishlist')

"""Views for the wishlist app."""
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Wishlist, wish_list
from products.models import Product
from django.contrib.auth.models import User
from user.models import UserProfile

from django.template.loader import render_to_string

#add wishlist by Ajax
@login_required(login_url='/login') # Check login
def add_wishlist(request):
    pid=request.GET['product']
    #pvariant=request.GET['pvariant']
    product=Product.objects.get(pk=pid)
    #print(product)
    data={}
    checkw=wish_list.objects.filter(product=product,user=request.user).count()
    print(checkw)
    if checkw > 0:
        print("already add to wish list")
        data={
			'bool':False,
		}
    else:
        Wish_list=wish_list.objects.create(
			product=product,
            
			user=request.user

		)
        wlistcount=wish_list.objects.filter(user=request.user).count()
        
        data={
			'bool':True,
            'wlcount':wlistcount,
		}
    return JsonResponse(data)
    #return JsonResponse({'bool':True})
#test from Code Artisan Lab
def add_wishlist_session_1(request):
    #del request.session['favodata']
    #del request.session['favo_p']
    favo_p={}
    favo_p[str(request.GET['p_id'])]={
        'pid':request.GET['p_id'],
		# 'image':request.GET['p_image'],
		# 'title':request.GET['p_title'],
		# 'qty':request.GET['p_qty'],
		# 'price':request.GET['p_price'],
	}
    #request.session['favo_p']=favo_p
    if 'favodata' in request.session:
        if str(request.GET['p_id']) in request.session['favodata']:
            print("you have already in favo list")
            #message.info(request,"you have already in favo list")
        else:
            #Not have in session favodata
            favo_data=request.session['favodata']
            favo_data.update('favo_p')
            #favo_data.session.modified=True
            request.session['favodata']=favo_data
            # add p_id to favo_data to wishlist
            #w_sess_list=get_object_or_404(wish_list,product_id=int(request.GET['p_id']))
            #request.session['favo_p']=favo_p
    else:
        request.session['favodata']=favo_p        
    #return JsonResponse({'data':request.session['favodata'],'totalitems':len(request.session['favodata'])})
    return JsonResponse({'data':request.session['favodata'],'totalitems':len(request.session['favodata'])})

from .wishsession import Wishsession
def add_wishlist_session(request):
    #get wish session
    wish_sess=Wishsession(request)
    #Get p_id from ajax
    p_id=int(request.GET['p_id'])
    # Lookup product in DB
    get_product = get_object_or_404(Product,id=p_id)
    # Save to Session
    wish_sess.add(product=get_product)
    # Count product in Session or quantiy of items
    wish_count=wish_sess.__len__()
    
    #Return response
    response=JsonResponse({'bool':True,'product_id':get_product.id,'wish_count':wish_count})
    return response

def view_wishlist_sess(request):
    #Get wishlist
    wish_list_sess_prods=Wishsession(request)
    
    wish_sess_products=wish_list_sess_prods.wish_list_session
    context={
        'wish_sess_products':wish_sess_products,
    }
    return render(request,'wishlist_display.html',context)

def delete_from_wishlist_sess(request):
    #Get wish list sess
    wish_list_sess_prods=Wishsession(request)
    #Get product id from ajax
    w_id=int(request.POST['wid'])
    # Deleted product id in Sess
    wish_list_sess_prods.delete_pro_sess(w_id)
    wish_count=wish_list_sess_prods.__len__()
    
    response=JsonResponse({'status':1,'wish_count':wish_count})
    return response
    
    

@login_required(login_url='/login') # Check login
def my_wishlist(request):
    wlist=wish_list.objects.filter(user=request.user)
    wlistcount=wish_list.objects.filter(user=request.user).count()
    
    
    #shopcart = ShopCart.objects.filter(user=request.user,)
   
    # for wl in wlist:
    #     for sc in shopcart:
    #         if wl.product==sc.product:
    #            pass 
    #         else:
    #             pass
    context={
       'wlist':wlist,
       'wlistcount':wlistcount,
      
    }
    return render(request,'wishlist_display.html',context)

# delete wishlist by ajax
#@login_required(login_url='/login') # Check login
def delete_from_wishlist(request):
    w_id=str(request.POST['wid'])
    #requestGET
    #w_id=str(request.GET['wid'])
    get_wid=wish_list.objects.get(pk=w_id)
    get_wid.delete()
    wlistcount=wish_list.objects.filter(user=request.user).count()
    #data={'status'}
    #t=render_to_string('wish_list_del_response.html')
    return JsonResponse({'status':1,'wlcount':wlistcount})
    
   