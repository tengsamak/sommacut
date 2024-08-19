from .cart_session import Cartsession,Cartsession_no_var

def cartsession(request):
    return {'cartsession':Cartsession(request)}



# add test for header
# from django.shortcuts import render
# def cart_header_sess(request):
#         check_cart_sess =''
#         cart_list_sess_prods=Cartsession(request)
#         cart_list_sess_no_var=Cartsession_no_var(request)
#         if cart_list_sess_prods and not cart_list_sess_no_var:
#                 check_cart_sess = 'cart_var'
#                 #after update:
#                 cartcount_sess=cart_list_sess_prods.__len__()
#                 cart_sess_products_var=cart_list_sess_prods.cart_list_session_var
#                 cart_pro_qty=cart_list_sess_prods.get_qty_var
#                 gettotal_no_var=cart_list_sess_no_var.get_total_no_var
#                 gettotal_var=cart_list_sess_prods.get_total_var
#                 context={
#                 'count_sess':cartcount_sess,
#                 'check_cart_sess':check_cart_sess,
#                 'cart_sess_products_var':cart_sess_products_var,
#                 'cart_pro_qty': cart_pro_qty,
#                 'grandtotal_sess':gettotal_var,
                
#                 }
#         elif cart_list_sess_no_var  and not cart_list_sess_prods : 
#                 check_cart_sess = 'cart_no_var'
#                 #after updated
#                 cartcount_sess=cart_list_sess_no_var.__len__()
#                 cart_list_sess_prods_no_var=cart_list_sess_no_var.cart_list_session_no_var
#                 cart_pro_qty_no_var=cart_list_sess_no_var.get_qty_no_var
#                 gettotal_no_var=cart_list_sess_no_var.get_total_no_var
#                 context={
#                 'count_sess':cartcount_sess,
#                 'check_cart_sess':check_cart_sess,
#                 'cart_list_sess_prods_no_var':cart_list_sess_prods_no_var,
#                 'cart_pro_qty_no_var':cart_pro_qty_no_var,
#                 'grandtotal_sess':gettotal_no_var,
#                 }
#         elif cart_list_sess_prods and cart_list_sess_no_var:
#                 check_cart_sess = 'both'
#                 #after updated
#                 cartcount_sess=cart_list_sess_prods.__len__() + cart_list_sess_no_var.__len__()
#                 cart_sess_products_var=cart_list_sess_prods.cart_list_session_var
#                 cart_pro_qty=cart_list_sess_prods.get_qty_var
#                 gettotal_var=cart_list_sess_prods.get_total_var()
                
#                 cart_list_sess_prods_no_var=cart_list_sess_no_var.cart_list_session_no_var
#                 cart_pro_qty_no_var=cart_list_sess_no_var.get_qty_no_var
#                 gettotal_no_var=cart_list_sess_no_var.get_total_no_var()
#                 grandtotal_sess=gettotal_var + gettotal_no_var
#                 context={
#                 'count_sess':cartcount_sess,
#                 'check_cart_sess':check_cart_sess,
#                 'cart_sess_products_var':cart_sess_products_var,
#                 'cart_pro_qty': cart_pro_qty,
#                 'cart_list_sess_prods_no_var':cart_list_sess_prods_no_var,
#                 'cart_pro_qty_no_var':cart_pro_qty_no_var,
#                 'grandtotal_sess':grandtotal_sess,
#                 }
#         else:
#                 #messages.info(request,"don't have cart in session")
#                 context={ 
#                 'check_cart_sess': "None",
                
#                 }
#         #return JsonResponse(context)
#         return render(request,'header.html',context)