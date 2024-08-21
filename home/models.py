from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.html import mark_safe
# Create your models here.
from django.forms import ModelForm, TextInput, Textarea

#for multilanguages
class Language(models.Model):
    name= models.CharField(max_length=20)
    code= models.CharField(max_length=5)
    #flag=models.ImageField(blank=True,upload_to='images/')
    create_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_at=models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.name

#for filter the true language select and update to langlist
llist = Language.objects.filter(code="en")
list1 = []
for rs in llist:
    list1.append((rs.code, rs.name))
langlist = (list1)

class Setting(models.Model):
    STATUS=(
        ('True','True'),
        ('False','False'),
    )
    #paymentlist=models.ForeignKey(Paymentlist,on_delete=models.CASCADE)
    title= models.CharField(max_length=150)
    keywords=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    company=models.CharField(max_length=100)
    address=models.CharField(blank=True,max_length=200)
    phone=models.CharField(max_length=20,blank=True)
    #fax=models.CharField(max_length=20,blank=True)
    email=models.CharField(blank=True,max_length=50)
    #smtpserver=models.CharField(blank=True,max_length=20)
    #smtpemail=models.CharField(blank=True,max_length=20)
    #smtppassword=models.CharField(blank=True,max_length=10)
    #smtpport=models.CharField(blank=True,max_length=5)
    logo=models.ImageField(blank=True,upload_to='images/logo')
    icon=models.ImageField(blank=True,upload_to='images/')
    # facebook=models.CharField(blank=True,max_length=50)
    # instagram=models.CharField(blank=True,max_length=50)
    # twitter=models.CharField(blank=True,max_length=50)
    # youtube = models.CharField(blank=True, max_length=50)
    #socialmedia = models.ForeignKey(SocialMedia,on_delete=models.CASCADE)
    aboutus=RichTextUploadingField(blank=True)
    contact=RichTextUploadingField(blank=True)
    termofservice =RichTextUploadingField(blank=True) 
    privacypolicy = RichTextUploadingField(blank=True)
    references=RichTextUploadingField(blank=True)
    status=models.CharField(max_length=10,choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_at=models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.title
    
class SocialMedia(models.Model):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    facebook=models.CharField(blank=True,max_length=50)
    instagram=models.CharField(blank=True,max_length=50)
    twitter=models.CharField(blank=True,max_length=50)
    youtube = models.CharField(blank=True, max_length=50)
    telegram=models.CharField(blank=True, max_length=50)
    
# class for text form contact information message
class ContactMessage(models.Model):
    STATUS=(
        ('New','New'),
        ('Read','Read'),
        ('Closed','Close'),
    )
    name=models.CharField(blank=True,max_length=20)
    email=models.CharField(blank=True,max_length=50)
    subject=models.CharField(blank=True,max_length=50)
    message=models.TextField(blank=True,max_length=255)
    status=models.CharField(blank=True,max_length=20,choices=STATUS,default='New')
    ip=models.CharField(blank=True,max_length=20)
    note=models.CharField(blank=True,max_length=100)
    create_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_at=models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.name

# Class create the form contact message
class ContactForm(ModelForm):
    class Meta:
        model=ContactMessage
        fields=['name','email','subject','message']
        widgets={
            'name':TextInput(attrs={'class':'input','placeholder':'Name & Surname'}),
            'subject':TextInput(attrs={'class':'input','placeholder':'Subject'}),
            'email': TextInput(attrs={'class': 'input', 'placeholder': 'Email Address'}),
            'message': Textarea(attrs={'class': 'input', 'placeholder': 'Your message','row':'5'}),

        }

class FAQ(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    lang = models.CharField(max_length=6, choices=langlist, blank=True, null=True)  # for multi languages
    ordernumber = models.IntegerField()
    question = models.CharField(max_length=200)
    answer = RichTextUploadingField()
    status=models.CharField(max_length=10, choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_at=models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.question



# class SettingLang(models.Model):
#     setting = models.ForeignKey(Setting, on_delete=models.CASCADE) #many to one relation with Category
#    # lang = models.CharField(max_length=6, choices=langlist)  # select from langlist above
#     title = models.CharField(max_length=150)
#     keywords = models.CharField(max_length=255)
#     description = models.CharField(max_length=255)
#     aboutus = RichTextUploadingField(blank=True)
#     contact = RichTextUploadingField(blank=True)
#     references = RichTextUploadingField(blank=True)
#     def __str__(self):
#         return self.title

#create slider image
from ckeditor.fields import RichTextField
class slider(models.Model):
    STATUS =(
        ("Expired","Expired"),
        ("Valid","Valid"),     
        ("Invalid","Invalid"),  
    )
    image=models.ImageField(upload_to="uploads/slider", max_length=None,help_text="192x550")
    headerslide = models.CharField(max_length=200,help_text="ex:For Summer, for Holiday.. ",blank=True)
    titleslide = models.CharField(help_text="Your Main Popose for slid, ex:Discount 20%, Sale off, Free Delivery..",max_length=100,blank=True)
    descriptionslid = models.CharField(max_length=300,help_text="detail about your promotion slide",blank=True)
    linkslide = models.CharField(max_length=500,help_text="link to product or link to vendor product list",blank=True)
    startdate = models.DateField(help_text="Start date to post Slide image",blank=True)
    finishdate = models.DateField(help_text="Finish date for promotion",blank=True)
    statusslide = models.CharField(choices=STATUS,max_length=100,blank=True)
    supportedby = models.CharField(help_text="Vendor Name",max_length=500,blank=True)
    slideterm = RichTextField(help_text="detail about contact vendor with developer on slide show, design and date post or expire",blank=True)
    
    def __self__(self):
        return self.supportedby
    def countday(sdate,fdate):
        day=fdate - sdate +1
        return day
    def image_tag(self):
        #img = Images.objects.get(id=self.image_id)
        if self.image is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""
    
    
class banner(models.Model):
    STATUS =(
        ("Expired","Expired"),
        ("Valid","Valid"),     
        ("Invalid","Invalid"),  
    )
    image=models.ImageField(upload_to="uploads/banner", max_length=None,help_text="958x401 or 960x401")
    name = models.CharField(help_text="Your Main Popose for banner, ex:Discount 20%, Sale off, Free Delivery..",max_length=100,blank=True)
    description = models.CharField(max_length=300,help_text="detail about your promotion slide",blank=True)
    link = models.CharField(max_length=500,help_text="link to product or link to vendor product list",blank=True)
    startdate = models.DateField(help_text="Start date to post banner image",blank=True)
    finishdate = models.DateField(help_text="Finish date for promotion",blank=True)
    status = models.CharField(choices=STATUS,max_length=100,blank=True)
    supportedby = models.CharField(help_text="Vendor Name or Admin",max_length=500,blank=True)
    term = RichTextField(help_text="detail about contact vendor with developer on Banner show, design and date post or expire",blank=True)
    
    def __self__(self):
        return self.supportedby
    def countday(sdate,fdate):
        day=fdate - sdate +1
        return day
    def image_tag(self):
        #img = Images.objects.get(id=self.image_id)
        if self.image is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""    
        
# payment for investor setting
class Paymentlist(models.Model):
    currency=(
        ("$","$"),
        ("៛","៛"),      
    )
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    bankname = models.CharField(default="Bank's Name",help_text="Bank Name",max_length=100,blank=True)       
    image_khqr = models.ImageField(upload_to="payment/",null=True) 
    image_dollaqr = models.ImageField(upload_to="payment/",null=True) 
    ratetoday = models.CharField(default="4100",null=True,help_text="Exchange Rate",max_length=100)
    def __self__(self):
        return self.setting
    