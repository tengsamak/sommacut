from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
# Register your models here.
from .models import ShopCart, OrderProduct, Order
#for pdf print
from django.urls import reverse
from django.utils.safestring import mark_safe


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product','user','quantity','price','amount', ]
    list_filter = ['user']







class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user','product','price','quantity','amount')
    can_delete = False
    extra = 0


#for pdf print
def order_pdf(obj):
    # pass
	return mark_safe('<a href="{}">PDF</a>'.format(reverse('admin_order_pdf',args=[obj.id])))

order_pdf.short_description = 'Order PDF'
#


#style order import export pdf
class OrderAdmin(ImportExportActionModelAdmin):
    list_display = ['id','code','first_name','last_name','phone','city','total','status','userordernote',order_pdf,]
    list_filter = ['status']
    readonly_fields = ('code','user','address','city','country','phone','first_name','last_name','ip','phone','city','total','userordernote')
    inlines = [OrderProductline]
    can_delate = False





class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user','product','price','quantity','amount','status','order',]
    list_filter = ['user','product','status','order']





admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)
admin.site.register(Order,OrderAdmin)
