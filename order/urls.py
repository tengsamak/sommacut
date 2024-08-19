from django.urls import path
from . import views
app_name = 'order'
urlpatterns = [
    path('',views.index,name='index'),
    #path('category_products/',views.category_products),
    path('addtoshopcart/<int:id>',views.addtoshopcart,name='addtoshopcart'),
    path('shopcart/',views.shopcart,name='shopcart'),
    path('deletefromcart/<int:id>',views.deletefromcart,name='deletefromcart'),
    #delete from cart by ajax
    path('delete_from_cartlist',views.delete_from_cartlist,name='delete_from_cartlist'),
    
    path('orderproduct/',views.orderproduct,name='orderproduct'),
    #updatecart by Ajax
    path('updatecart',views.updatecart,name='updatecart'),
    # Add to Cart by Ajax with No variant (add_tocart_no_variant) 
    path('add_tocart_no_variant',views.add_tocart_no_variant,name='add_tocart_no_variant'),
    # Add to Cart by Ajax with variant (add_tocart_with_variant)
    path('add_tocart_with_variant',views.add_tocart_with_variant,name='add_tocart_with_variant'),
    
    #CartListAjax on Header cartlistajax
    path('cartlistajax',views.cartlistajax,name='cartlistajax'),
    # apply promotcode for shopcart ajax
    path('applypromo',views.promoapply, name="promoapply"),
    #test checkout
    path('checkout',views.checkout, name="checkout"),
    # checkoutcompleted
    path('checkoutcompleted',views.checkoutcompleted, name="checkoutcompleted"),
    #testfrmcompleted
    path('testfrmcompleted',views.testfrmcompleted, name="testfrmcompleted"),
    # checkphone number modals
    path('checkphone',views.checkphone, name="checkphone"),
    # OTP verify check 
    path('otpverify',views.otp_view,name='otp_phone'),
    # checkoutcompleted refesh page
    path('checkoutcompleted_2/<ordercode>',views.checkoutcompleted_2, name="checkoutcompleted_2"),
    
    # for pdf print weasyprint
    # path('admin/order/(?P<order_id>\d+)/pdf/$',views.admin_order_pdf,name='admin_order_pdf'),
    path('admin/order/<order_id>/pdf',views.admin_order_pdf,name='admin_order_pdf'),
    #for invoice pdf
    path('generate/pdf/<ordercode>/', views.generate_pdf, name='generate_pdf'),
    #invoiceprint
    path('invoiceprint/<ordercode>', views.invoiceprint, name='invoiceprint'),
    
    #Receiptprint
    path('receiptprint/<ordercode>', views.receiptprint, name='receiptprint'),
    
    #add Cart Session add_cart_session with NO Variant
    path('add_cart_session_no_var/',views.add_cart_session_no_var,name='add_cart_session_no_var'),
    #add to Cart session add_cart_session_var with Variant
    path('add_cart_session_var/',views.add_cart_session_var,name='add_cart_session_var'),
    # view Cart List Session view_cartlist_sess
    path('view_cartlist_sess/',views.view_cartlist_sess,name='view_cartlist_sess'),
    # del Cart List Session No_var
    path('del_cart_sess_no_var/',views.del_cart_sess_no_var,name='del_cart_sess_no_var'),
    #del_cart_sess_var
    path('del_cart_sess_var/',views.del_cart_sess_var,name='del_cart_sess_var'),
    #Update_cart_sess
    path('update_cart_sess/',views.updatecart_sess,name='updatecart_sess'),
    #header_cart_list_sess
    path('header_cartlist_sess/',views.header_cartlist_sess,name='header_cartlist_sess'),
    #checkout_sess
    path('checkout_sess',views.checkout_sess, name="checkout_sess"),
    # checkoutcompleted_sess
    path('checkoutcompleted_sess',views.checkoutcompleted_sess, name="checkoutcompleted_sess"),
    #checkoutcompleted_2_sess for refresh page
    path('checkoutcompleted_2_sess/<ordercode>',views.checkoutcompleted_2_sess, name="checkoutcompleted_2_sess"),
    #Receiptprint session
    path('receiptprint_sess/<ordercode>', views.receiptprint_sess, name='receiptprint_sess'),
    #invoiceprint session
    path('invoiceprint_sess/<ordercode>', views.invoiceprint_sess, name='invoiceprint_sess'),
]