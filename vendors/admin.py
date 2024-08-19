from django.contrib import admin

# Register your models here.
from products.models import Product

from vendors.models import Vendor,Comment_v
#from django.utils.safestring import mark_safe
import admin_thumbnails


class VendorProductInline(admin.TabularInline):
    model = Product
    #readonly_fields = ('id')
    fields = ['category','id','title','variant']
    #list_display = ['category','id','title','variant']
    # readonly_fields = ['id','category','title','variant']



#@admin_thumbnails.thumbnail('logo')
class VendorAdmin(admin.ModelAdmin):
    readonly_fields =('logo_tag',)
    list_display =['companyname','address1','contactname','phone1','status','create_at','logo_tag','facebook','ig','APM','email','tiktok',]
    list_filter = ['status','companyname']
    inlines = [VendorProductInline]
    
    # def logo_tag(self,obj):
    #     return mark_safe('<img src="{url}" height="50"/>'.format(url=obj.logo.url))
        
class Comment_v_Admin(admin.ModelAdmin):
    list_display = ['id','subject_v','comment_v','rate_v', 'status','create_at','vendor_id','user']
    list_filter = ['status']
    readonly_fields = ('subject_v','comment_v','ip','user','vendor','rate_v','id')



admin.site.register(Vendor,VendorAdmin)
admin.site.register(Comment_v,Comment_v_Admin)