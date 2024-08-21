from django.utils import timezone
import pytz
#from datetime import datetime,timedelta #change timezone
from django.utils.timezone import datetime,timedelta
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager


# Create your models here.
# from django.utils.safestring import mark_safe
from django.db.models import Avg, Count
from django.forms import ModelForm
from django.urls import reverse
from django.utils.html import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from vendors.models import Vendor

from .utils import generate_pro_code
# from home.models import Language


class Category(MPTTModel):   # we use mptt so we need to change models.Model to MPTTModel
    STATUS=(
        ('True','True'),
        ('False','False'),
    )
    # we use mptt so we change ForeignKey to TreeForeignKey
    #parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    title= models.CharField(max_length=30)
    keywords=models.CharField(max_length=255)
    description= models.CharField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=10,choices=STATUS)

   # slug= models.SlugField()  # for urls by string this slug we create by own or copy
    slug = models.SlugField(null=False,unique=True)  # This slug will for create auto when we have many products
                                                    # with the relate function name get_absolute_url below
    create_at=models.DateTimeField(auto_now_add=True,blank=True)
    update_at=models.DateTimeField(auto_now=True,blank=True)

    class MPTTMeta:
       # level_attr = 'mptt_level'
        order_insertion_by = ['title']
        
    class Meta:    
        verbose_name ="Category"
        verbose_name_plural ="Categories"

    def __str__(self):
        return self.title

    # function ដើម្បីបែងចែកProducts ស្ថិតនៅ Category មួយណាស្រួលមើលពេល Add products and selected catgegory
    def __str__(self):              # __str__ method elaborated later in
        full_path = [self.title]    # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

    def get_absolute_url(self):
        return reverse('category_detail',kwargs={'slug':self.slug})
    
    


class Product(models.Model):
    STATUS=(
        ('True','True'),
        ('False','False'),
        #('New','New'),
    )
    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )
    VENDOR=(
        ('Yes','Yes'),
        ('NO','NO'),
    )
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='categ',blank=True) # we have many to one relation to Category table
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE,blank=True) #relation one Vendor have Many products
    title=models.CharField(max_length=255)
    title_kh=models.CharField(max_length=255) # title in KH (remove keyword)
    pro_code=models.CharField(max_length=5,blank=True,help_text="Product Code auto generated") #for create product code
    description=models.CharField(max_length=255)
    image=models.ImageField(upload_to='images/products/',null=False)
    price=models.DecimalField(max_digits=12, decimal_places=2,default=0,help_text="Sale price",blank=False)
    m_price=models.DecimalField(max_digits=12, decimal_places=2,default=0,help_text="Market Price or Regular price",blank=False)
    # price-old=models.FloatField()
    amount=models.IntegerField()
    minamount=models.IntegerField()  # make sum amount
    variant = models.CharField(max_length=10, choices=VARIANTS, default='None')
    detail=RichTextUploadingField() # after add cdeditor we change the detail_field to RichTextUploadingField() of ckeditor
    #slug=models.SlugField()  # this will create slug by own user input when add products
    slug = models.SlugField(null=False,unique=True) # This will create auto slug by own name products
    status=models.CharField(max_length=10,choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_at=models.DateTimeField(auto_now=True,blank=True,null=True)
    tags = TaggableManager()
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('products_detail',kwargs={'slug':self.slug})
    
    #for generate product code
    def save(self,*args, **kwargs):
        if self.pro_code == "":
            self.pro_code = generate_pro_code() # import function from utils.py
        return super().save(*args,**kwargs)
            
            



    # function to create a fake table field in read only mode in admin mode products
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""
    #image_tag.short_description='Image'

    def avaregereview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(avarage=Avg('rate'))
        avg = 0
        if reviews["avarage"] is not None:
            avg = float(reviews["avarage"])
        return avg

    def countreview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt
    # def countproduct(vid):
    #     #vendorprocount=Product.objects.values('vendor_id').annotate(count=Count('vendor_id')).filter(status=True)
    #     vendorprocount=Product.objects.filter(status=True,vendor_id=vid).values('vendor_id').annotate(count=Count('vendor_id'))
    
    #     vnt = int(vendorprocount["count"])
    #     return vnt
    
    def newstatus(self):
        #tz = pytz.timezone('America/New_York')
        utc = pytz.UTC
        check=self.create_at + timedelta(days=60)
        #dt_aware = datetime(2024, 9, 20, 12, 0, 0, tzinfo=tz).replace(tzinfo=utc)
        #convert data time in check for the same UTC in order to compare
        dt_aware_check=check.replace(tzinfo=utc)
        
        today=datetime.now()
        dt_naive_today=today.replace(tzinfo=utc)
        #now = timezone.now()
        if dt_aware_check >= dt_naive_today:
            pro_status="New"
        else:
            pro_status="True"
        #print("********my statuse**********",pro_status)    
        return pro_status
    # M market price s selling price
    def discount_percentage(self):
        fraction = self.price / self.m_price
        discount_fraction = 1 - fraction
        percentage = discount_fraction * 100
        return f"{percentage:.2f}%"
    
    #countdowon discount time on product
    # def discount_timer(self):
        
    #     fraction = self.price / self.m_price
    #     discount_fraction = 1 - fraction
    #     percentage = discount_fraction * 100
    #     return f"{percentage:.2f}%"
    
    
    # def gapprice(self): # between market price and price
    #     if self.variant =='None':
    #         gapprice_ = self.m_price - self.price
    #     else:
    #         gapprice_ = self.m_price - Variants.objects.get(self.id)
        
    #     return f"{gapprice_:.2f}"
class Event_timer(models.Model):
    STATUS=(
        ('Active','Active'), # ongoing event
        ('False','False'), # turnoff
        ('Expired','Expired'), # return the price = m.price
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True) 
    end_date=models.DateTimeField(auto_now=True,blank=True,help_text="Please select Furture date and time from now to countdown",null=True)
    status=models.CharField(max_length=10,blank=True,default="False")
    create_at=models.DateTimeField(auto_now=True,blank=True,null=True)
    def __str__(self):
        return self.product.pro_code
    
    def discount_timer(self):
        
        if self.end_date >= timezone.now() :
            self.status = "Active" 
            self.save()
            # fraction = self.product.price / self.product.m_price
            # discount_fraction = 1 - fraction
            # percentage = discount_fraction * 100
            #return f"{percentage:.2f}%"
            return self.status
        else:
            self.status = "Expired"
            self.save()
            #set product price = m.price
            
            # pro_price = Product.objects.get(id=self.product.id)
            # pro_price.price = pro_price.m_price
            # pro_price.save()
            
            # fraction = self.product.price / self.product.m_price
            # discount_fraction = 1 - fraction
            #percentage = 0
            #return f"{percentage:.2f}%"
            return self.status
    
# create class images for add more images in a product image
class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE) # Many to One Relationship a product have many images
    title=models.CharField(max_length=50,blank=True)
    image=models.ImageField(blank=True,upload_to='images/products/')
    
    class Meta:
        verbose_name ="Image"
        verbose_name_plural ="Images"

    def __str__(self):
        return self.title
    
    def image_tag(self):
        #img = Images.objects.get(id=self.image_id)
        if self.image is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True)
    #vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status=models.CharField(max_length=10,choices=STATUS, default='True')
    create_at=models.DateTimeField(auto_now_add=True,blank=True)
    update_at=models.DateTimeField(auto_now=True,blank=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject','comment','rate']


class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name
   # @property
    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name


class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    image_id = models.IntegerField(blank=True,null=True,default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    
    class Meta:
        verbose_name ="Variant"
        verbose_name_plural ="Variants"

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            varimage=img.image.url
        else:
            varimage=""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""
    # @property #added from product
    # def price(self):
    #     if self.product_id is not None:
    #         return (self.product.price)


# llist= Language.objects.all()
# list1=[]
# for rs in llist:
#     list1.append((rs.code,rs.name))
# langlist= (list1)
# #for multilanguage
# class ProductLang(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE) #many to one relation with Category
#     lang =  models.CharField(max_length=6, choices=langlist)
#     title = models.CharField(max_length=150)
#     keywords = models.CharField(max_length=255)
#     description = models.CharField(max_length=255)
#     slug = models.SlugField(null=False, unique=True)
#     detail=RichTextUploadingField()
#
#     def get_absolute_url(self):
#         return reverse('product_detail', kwargs={'slug': self.slug})
#
# #for multilanguage
# class CategoryLang(models.Model):
#     category = models.ForeignKey(Category, related_name='categorylangs', on_delete=models.CASCADE) #many to one relation with Category
#     lang =  models.CharField(max_length=6, choices=langlist)
#     title = models.CharField(max_length=150)
#     keywords = models.CharField(max_length=255)
#     slug = models.SlugField(null=False, unique=True)
#     description = models.CharField(max_length=255)
#
#     def get_absolute_url(self):
#         return reverse('category_detail', kwargs={'slug': self.slug})