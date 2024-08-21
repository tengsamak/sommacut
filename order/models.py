from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm
#from django_simple_coupons.models import Coupon
from products.models import Product

from products.models import Variants

from coupons.models import Coupons
from phonenumber_field.modelfields import PhoneNumberField


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True) # relation with varinat
    quantity = models.IntegerField(blank=True)

    """add from coupon"""
    # def __init__(self, request):
    #     """initalize the ShopCart"""
    #     self.session = request.session
    #     shopcart = self.session.get(settings.CART_SESSION_ID)

        # if not shopcart:
        #     shopcart = self.session[settings.CART_SESSION_ID] = {}
        # self.shopcart = shopcart
        # self.coupon_id = self.session.get('coupon_id')

    """End add from coupon"""


    def __str__(self):
        return self.product.title

    @property
    def price(self):
        if self.product_id is not None:
            return (self.product.price)
        
    @property
    def m_amount(self): # for calc amount in Market Price 
        if self.product_id is None:
            return 'None'
        return (self.quantity * self.product.m_price)    

    @property
    def amount(self): # for sale price
        if self.product_id is None:
            return 'None'
        return (self.quantity * self.product.price)

    @property
    def varamount(self):
        if self.variant_id is None:
            return 'None'
        return (self.quantity * self.variant.price)

# /////insert from cart.py code of coupons project//////////////
    """docstring for Cart"""


    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        del self.session['coupon_id']
        self.session.modified = True

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupons.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()


# end insert////////////////////////////


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']

#add for submit coupons code
# class CouponsForm(ModelForm):
#     class Meta:
#         model=Coupons
#         fields=['code']


class Order(models.Model):
    STATUS=(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Preaparing','Preaparing'),
        ('OnShipping','Onshipping'),
        ('Completed','Completed'),
        ('Canceled','Canceled'),
    )
    PAYMENT=(
        ('PAID','PAID'),
        ('UNPAID','UNPAID'),
    )
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    code=models.CharField(max_length=5,editable=False)
    first_name=models.CharField(max_length=10)
    last_name=models.CharField(max_length=10)
    #phone=models.CharField(blank=True,max_length=50)
    phone = PhoneNumberField(region="KH",help_text='Please input the phone number the used with telegram. EX:012 345 678')
    address=models.CharField(blank=True,max_length=500)
    email= models.EmailField(blank=True,max_length=50)
    total=models.FloatField(blank=True,max_length=150)
    vat10=models.FloatField(null=True,blank=True,max_length=150) #added
    grandtotal=models.FloatField(blank=True,max_length=150) #added
    discount=models.FloatField(null=True,max_length=50)# add for apply coupon code
    totalafterdiscount=models.FloatField(null=True,max_length=150)# add for apply coupon code
    vat10afterdiscount= models.FloatField(null=True,max_length=150) #added
    grandtotalafterdiscount=models.FloatField(null=True,max_length=150) #added
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    ip=models.CharField(blank=True,max_length=20)
    adminnote=models.TextField(blank=True,max_length=500)
    userordernote=models.TextField(blank=True,max_length=500) #add more samak
    paymentinfo=models.CharField(blank=True,max_length=150) #add more samak
    payment_mode=models.CharField(max_length=150,null=False,default='COD')#add more samak
    payment_id=models.CharField(max_length=250, null=True)#add more samak
    paymentstatus = models.CharField(max_length=10, choices=PAYMENT, default='UNPAID')
    tracking_no= models.CharField(null=True, max_length=150)
    rate_by_ordered = models.CharField(null=True,max_length=50)# record exchange rate while the date place order
    grandtotal_in_kh_real = models.FloatField(null=True,max_length=250) # record total in KH_real both discount and not discount
    create_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_at=models.DateTimeField(auto_now=True,blank=True,null=True)

    class Meta:
        # ordering = ('-created',)
        verbose_name = "order"
        verbose_name_plural = "orders"

    def __str__(self):
       # return self.user.first_name
       return 'order {}'.format(self.id)

#from django import forms
from django.forms import TextInput
# class phonenumberfrm(forms.Form):
#     phone = PhoneNumberField(region="KH",null=False, blank=False)
class OrderForm(ModelForm):
    class Meta:
        model=Order
        fields=['phone']
        widgets = {
            'phone':TextInput(attrs={'class': 'form-control','placeholder':'Your telegram phone number','type':'number','value':'+855','readonly':'readonly',}),
        }

class OrderProduct(models.Model):
    STATUS=(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Canceled','Canceled'),
        ('Session','Session'),
    )
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL, blank=True, null=True)  # relation with varinat
    quantity=models.IntegerField(blank=True)
    price=models.DecimalField(max_digits=12, decimal_places=2,default=0)
    amount=models.FloatField(blank=True,max_length=150) #about price
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    create_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_at=models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.product.title

    # @property
    # def amount(self):
    #     if self.product_id is None:
    #         return 'None'
    #     return (self.quantity * self.product.price)

    # @property
    # def varamount(self):
    #     if self.variant_id is None:
    #         return 'None'
    #     return (self.quantity * self.variant.price)

