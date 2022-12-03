from django.contrib import admin

# Register your models here.
from products.models import Product

from vendors.models import Vendor


class VendorProductInline(admin.TabularInline):
    model = Product
    # readonly_fields = ['id','category']
    fields = ['id','category','title','variant']
    # readonly_fields = ['id','category','title','variant']



class VendorAdmin(admin.ModelAdmin):
    list_display =['companyname','address','contactname','phone','status','create_at']
    list_filter = ['status','companyname']
    inlines = [VendorProductInline]


admin.site.register(Vendor,VendorAdmin)