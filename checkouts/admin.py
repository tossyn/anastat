from django.contrib import admin

from .models import *
# Register your models here.
class CheckoutAdmin(admin.ModelAdmin):
	list_display = ('transaction_id','time', 'payment_mode', 'payment_confirmed', 'affiliate_manager_approved', 'data_delivered', 'data_cost', 'cost_with_vats')
	
admin.site.register(Checkout, CheckoutAdmin)
 