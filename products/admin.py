import admin_thumbnails
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
#import admin_thumbnails

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Product, Images, Comment, Color, Size, Variants #, ProductLang, CategoryLang


# class CategoryLangInline(admin.TabularInline):
#     model = CategoryLang
#     extra = 1
#     show_change_link = True
#     prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','parent','status']
    list_filter = ['status']

# copy mptt admin from the website crate admin2
class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug':('title',)} # auto slug for category admin
   # inlines = [CategoryLangInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

# class ProductLangInline(admin.TabularInline):
#     model = ProductLang
#     extra = 1
#     show_change_link = True
#     prepopulated_fields = {'slug': ('title',)}

 # add more images in a products call from Images Class
@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 4

class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title','category','vendor','status','image_tag']
    list_filter = ['category','vendor']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline,ProductVariantsInline,]#ProductLangInline]
    prepopulated_fields = {'slug': ('title',)} #auto slug for products admin

@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image','title']




class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment','rate', 'status','create_at','product_id','user']
    list_filter = ['status']
    readonly_fields = ('subject','comment','ip','user','product','rate','id')


class ColorAdmin(ImportExportModelAdmin):
    list_display = ['name','code','color_tag']
    pass

class SizeAdmin(admin.ModelAdmin):
    list_display = ['name','code']
    list_filter = ['name']


@admin_thumbnails.thumbnail('image')
class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title','product','color','size','price','quantity','image_tag']
    list_filter = ['size','color']

# class ProductLangugaeAdmin(admin.ModelAdmin):
#     list_display = ['title','lang','slug']
#     prepopulated_fields = {'slug': ('title',)}
#     list_filter = ['lang']
#
# class CategoryLangugaeAdmin(admin.ModelAdmin):
#     list_display = ['title','lang','slug']
#     prepopulated_fields = {'slug': ('title',)}
#     list_filter = ['lang']

# class ProductVendorInline(admin.TabularInline):
#     model = Vendor
#     list_display=['companyname']
#     readonly_fields = ('id',)
#
# class VendorAdmin(admin.ModelAdmin):
#     list_display  =['companyname','phone','address','contactname','status','create_at']
#     list_filter = ['status','companyname']
#     inlines = [ProductVendorInline]
#
#
# admin.site.register(Vendor,VendorAdmin)
admin.site.register(Category,CategoryAdmin2)
admin.site.register(Product,ProductAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Variants,VariantsAdmin)
# admin.site.register(ProductLang,ProductLangugaeAdmin)
# admin.site.register(CategoryLang,CategoryLangugaeAdmin)