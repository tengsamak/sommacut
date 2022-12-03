from django.contrib import admin
from .models import Setting, ContactMessage, FAQ, Language


# Register your models here.
class SettingAdmin(admin.ModelAdmin):
    list_display = ['title','company','update_at','status']

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



admin.site.register(Setting,SettingAdmin)
admin.site.register(ContactMessage,ContactMessageAdmin)
admin.site.register(FAQ,FAQAdmin)
admin.site.register(Language,LanguagesAdmin)
# admin.site.register(SettingLang,SettingLangAdmin)