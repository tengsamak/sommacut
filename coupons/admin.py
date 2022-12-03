from django.contrib import admin

# Register your models here.
from coupons.models import Coupons


class CouponsAdmin(admin.ModelAdmin):
	'''
		Admin View for Coupons
	'''
	list_display = ('code','valid_from','valid_to','discount','active',)
	list_filter = ('active','valid_from','valid_to',)
	search_fields = ('code',)

admin.site.register(Coupons, CouponsAdmin)