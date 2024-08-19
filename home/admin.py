from django.contrib import admin
from .models import Setting, ContactMessage, FAQ, Language,slider,banner,Paymentlist, SocialMedia
import admin_thumbnails

# Register your models here.
class SettingAdmin(admin.ModelAdmin):
    list_display = ['title','company','update_at','status','termofservice','privacypolicy',]

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name','subject','update_at','status']
    readonly_fields = ('name','subject','email','message','ip') # because we get this information from customers
    list_filter = ['status']

class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer','ordernumber','status']
    list_filter = ['status','lang']

#for multi languages
class LanguagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'code',]#'status']
    list_filter = ['name']
#  #for multilanguages on settinglang
# class SettingLangAdmin(admin.ModelAdmin):
#     list_display = ['title', 'keywords','description','lang']
#     list_filter = ['lang']
@admin_thumbnails.thumbnail('image')
class SliderAdmin(admin.ModelAdmin):
    list_display =['image_tag','supportedby','titleslide','startdate','finishdate','statusslide']
    list_filter = ['supportedby']

@admin_thumbnails.thumbnail('image')
class BannerAdmin(admin.ModelAdmin):
    list_display =['image_tag','supportedby','name','startdate','finishdate','status']
    list_filter = ['supportedby']
    
class PaymentlistAdmin(admin.ModelAdmin):
    list_display = ['bankname', 'ratetoday',]#'status']
    list_filter = ['bankname']

class SocialmediaAdmin(admin.ModelAdmin):
    list_display = ['facebook', 'instagram','youtube','telegram']
    list_filter = ['telegram']

admin.site.register(banner,BannerAdmin)
admin.site.register(slider,SliderAdmin)
admin.site.register(Setting,SettingAdmin)
admin.site.register(ContactMessage,ContactMessageAdmin)
admin.site.register(FAQ,FAQAdmin)
admin.site.register(Language,LanguagesAdmin)
# admin.site.register(SettingLang,SettingLangAdmin)
admin.site.register(Paymentlist,PaymentlistAdmin)
admin.site.register(SocialMedia,SocialmediaAdmin)