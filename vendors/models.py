from django.contrib.auth.models import User
from django.db import models

# Create your models here.



class Vendor(models.Model):
    STATUS = (
        ('Active', 'Active'),
        ('New', 'New'),
        ('False', 'False'),
        ('Approved', 'Approved'),
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE)  # OneToOneField  is to ensure that one user have only one vendor
    companyname = models.CharField(max_length=500,null=True)
    phone = models.CharField(max_length=500,null=True)
    address = models.CharField(max_length=500,null=True,blank=True)
    contactname = models.CharField(max_length=500,null=True)
    logo = models.ImageField(upload_to='images/vendors/', blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True,blank=True)
    update_at = models.DateTimeField(auto_now=True,blank=True)

    def __str__(self):
        return self.companyname

