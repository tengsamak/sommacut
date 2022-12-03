from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput, Textarea

#for multilanguages
class Language(models.Model):
    name= models.CharField(max_length=20)
    code= models.CharField(max_length=5)
    #flag=models.ImageField(blank=True,upload_to='images/')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

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
    title= models.CharField(max_length=150)
    keywords=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    company=models.CharField(max_length=100)
    address=models.CharField(blank=True,max_length=200)
    phone=models.CharField(max_length=20,blank=True)
    fax=models.CharField(max_length=20,blank=True)
    email=models.CharField(blank=True,max_length=50)
    smtpserver=models.CharField(blank=True,max_length=20)
    smtpemail=models.CharField(blank=True,max_length=20)
    smtppassword=models.CharField(blank=True,max_length=10)
    smtpport=models.CharField(blank=True,max_length=5)
    icon=models.ImageField(blank=True,upload_to='images/')
    facebook=models.CharField(blank=True,max_length=50)
    instagram=models.CharField(blank=True,max_length=50)
    twitter=models.CharField(blank=True,max_length=50)
    youtube = models.CharField(blank=True, max_length=50)
    aboutus=RichTextUploadingField(blank=True)
    contact=RichTextUploadingField(blank=True)
    references=RichTextUploadingField(blank=True)
    status=models.CharField(max_length=10,choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

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
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

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
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

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