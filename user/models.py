
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe

# from home.models import Language


class UserProfile(models.Model):
    TYPE=(
        ('Normal','Normal'),
        ('Re-Seller','Re-Seller'),
        ('VENDOR', 'VENDOR'),
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    # user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    phone=models.CharField(blank=True,max_length=20)
    address=models.CharField(blank=True,max_length=150)
    city=models.CharField(blank=True,max_length=20)
    country=models.CharField(blank=True,max_length=20)
    image=models.ImageField(blank=True,upload_to='media/uploads/user')
    usernote=models.TextField(blank=True,max_length=500) #add more samak
    usertype=models.CharField(max_length=20,choices=TYPE,default="Normal")
    # language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True) # multi language on userprofile

    
        
    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' '+ self.user.last_name +' ['+ self.user.username+']'

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

 #   def updateuserprofile(self):
 
# Model for subcriber
from django.utils import timezone
class SubscribedUsers(models.Model):
    #name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    created_date = models.DateTimeField('Date created', auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.email

