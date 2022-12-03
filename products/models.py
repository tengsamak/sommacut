
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
# from django.utils.safestring import mark_safe
from django.db.models import Avg, Count
from django.forms import ModelForm
from django.urls import reverse
from django.utils.html import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from vendors.models import Vendor

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
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    class MPTTMeta:
       # level_attr = 'mptt_level'
        order_insertion_by = ['title']

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
    category=models.ForeignKey(Category,on_delete=models.CASCADE) # we have many to one relation to Category table
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE) #relation one Vendor have Many products
    title=models.CharField(max_length=150)
    keywords=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    image=models.ImageField(upload_to='images/products/',null=False)
    price=models.DecimalField(max_digits=12, decimal_places=2,default=0)
    # price-old=models.FloatField()
    amount=models.IntegerField()
    minamount=models.IntegerField()  # make sum amount
    variant = models.CharField(max_length=10, choices=VARIANTS, default='None')
    detail=RichTextUploadingField() # after add cdeditor we change the detail_field to RichTextUploadingField() of ckeditor
    #slug=models.SlugField()  # this will create slug by own user input when add products
    slug = models.SlugField(null=False,unique=True) # This will create auto slug by own name products
    status=models.CharField(max_length=10,choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('products_detail',kwargs={'slug':self.slug})



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


# create class images for add more images in a product image
class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE) # Many to One Relationship a product have many images
    title=models.CharField(max_length=50,blank=True)
    image=models.ImageField(blank=True,upload_to='images/products/')

    def __str__(self):
        return self.title


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status=models.CharField(max_length=10,choices=STATUS, default='New')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

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