from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.db.models import Avg, Count
from django.forms import ModelForm
#from django.utils.html import mark_safe

# Create your models here.



class Vendor(models.Model):
    STATUS = (
        ('Active', 'Active'),
        ('New', 'New'),
        ('Inactive', 'Inactive'),
        ('True', 'True'),
        ('False', 'False'),
        
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE)  # OneToOneField  is to ensure that one user have only one vendor
    follows=models.ManyToManyField("self",related_name="Followed_by",symmetrical=False,blank=True)
    companyname = models.CharField(max_length=500,null=True,help_text="Company Name")
    companydetail=models.TextField(null=True,help_text="Comapy Vision Mission and type of business")
    phone1 = models.CharField(max_length=500,null=True)
    phone2 = models.CharField(max_length=500,null=True)
    address1 = models.CharField(max_length=500,null=True,blank=True)
    address2 = models.CharField(max_length=500,null=True,blank=True)
    contactname = models.CharField(max_length=500,null=True)
    logo = models.ImageField(null=True, blank=True,upload_to='images/vendors/')
    pattern = models.ImageField(null=True,upload_to='images/vendors/', blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='True')
    create_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    email=models.EmailField(max_length=100,null=True)
    www=models.CharField(max_length=300,null=True)
    facebook=models.CharField(max_length=300,null=True)
    ig=models.CharField(max_length=300,null=True)
    tiktok=models.CharField(max_length=300,null=True)
    APM=models.TextField(null=True,help_text="Accepted Payment Method") # Accepted Payment Method
    startyear=models.CharField(max_length=10,null=True) # for business started date year
    maplocation=models.TextField(null=True,help_text="Google map passed link")
    
    
    class Meta:
        verbose_name ="Vendor"
        verbose_name_plural ="Vendors"

    def __str__(self):
        return self.companyname
    
    def logo_tag(self):
        #if self.logo is not None: 
        try:
            #return mark_safe('<img src="{}" height="50"/>'.format(self.logo))
            return format_html('<img src="{}" height="50"/>'.format(self.logo.url))
        except:
            pass
        #else:
        #    return "No Logo"
    logo_tag.short_description = 'logoTag'
    #logo_tag.allow_tags = True
    def avaregereview(self):
        reviews = Comment_v.objects.filter(vendor=self, status='True').aggregate(avarage=Avg('rate_v'))
        avg = 0
        if reviews["avarage"] is not None:
            avg = float(reviews["avarage"])
        return avg

    def countreview(self):
        reviews = Comment_v.objects.filter(vendor=self, status='True').aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt
        

class Comment_v(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    #product=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True)
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject_v = models.CharField(max_length=50, blank=True)
    comment_v = models.CharField(max_length=250,blank=True)
    rate_v = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status=models.CharField(max_length=10,choices=STATUS, default='True')
    create_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_at=models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.status
    
class CommentForm_v(ModelForm):
    class Meta:
        model = Comment_v
        fields = ['subject_v','comment_v','rate_v']    