from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm
from django_simple_coupons.models import Coupon
from products.models import Product

from products.models import Variants

from coupons.models import Coupons


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True) # relation with varinat
    quantity = models.IntegerField()

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
    def amount(self):
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
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    code=models.CharField(max_length=5,editable=False)
    first_name=models.CharField(max_length=10)
    last_name=models.CharField(max_length=10)
    phone=models.CharField(blank=True,max_length=20)
    address=models.CharField(blank=True,max_length=150)
    city=models.CharField(blank=True,max_length=20)
    country=models.CharField(blank=True,max_length=20)
    total=models.FloatField()
    vat10=models.FloatField() #added
    grandtotal=models.FloatField() #added
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    ip=models.CharField(blank=True,max_length=20)
    adminnote=models.TextField(blank=True,max_length=500)
    userordernote=models.TextField(blank=True,max_length=500) #add more samak
    paymentinfo=models.CharField(blank=True,max_length=150) #add more samak
    paymentstatus = models.CharField(max_length=10, choices=PAYMENT, default='UNPAID')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    class Meta:
        # ordering = ('-created',)
        verbose_name = "order"
        verbose_name_plural = "orders"

    def __str__(self):
       # return self.user.first_name
       return 'order {}'.format(self.id)


class OrderForm(ModelForm):
    class Meta:
        model=Order
        fields=['first_name','last_name','address','phone','city','country','userordernote','adminnote','paymentinfo',]

class OrderProduct(models.Model):
    STATUS=(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Canceled','Canceled'),
    )
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL, blank=True, null=True)  # relation with varinat
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=12, decimal_places=2,default=0)
    amount=models.FloatField()
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title

