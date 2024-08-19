
#**************
import random
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
    vat10 = total * decimal.Decimal(0.10)  # convert float to decimal
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
        #form = OrderForm(request.POST)
        # return HttpResponse(request.POST.items())
        #if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............

        data = Order()
        data.first_name = request.POST.get('first_name')  # get product quantity from form
        data.last_name = request.POST.get('last_name')
        data.email = request.POST.get('email')
        data.address = request.POST.get('address')
        data.phone = request.POST.get('phone')    
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
        return HttpResponseRedirect(reverse('order:checkoutcompleted_2', args=(ordercode,)))
        #return HttpResponseRedirect(reverse('order:invoiceprint', args=(ordercode,)))
    elif ShopCart.objects.filter(user_id=current_user.id).exists():
        messages.warning(request, "you errors please checkout again or contact us")
        return HttpResponseRedirect(reverse('order:checkout'))
    # elif Order.objects.filter(user_id=current_user.id,code=ordercode).exists():
    #     messages.info(request,"your order completed and check your invoice")
    #     return HttpResponseRedirect(reverse('order:invoiceprint', args=(ordercode,)))
    else:
        messages.info(request,"Please check you account for your order, And continues shopping!")
        return HttpResponseRedirect('/')
    
    #return HttpResponseRedirect(/)