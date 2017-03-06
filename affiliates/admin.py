from django.contrib import admin
from affiliates.models import *
# Register your models here.
class InstitutionAdmin(admin.ModelAdmin):
	list_display = ('name', 'code', 'manager')
	#fields = (('name', 'code'), 'content')
admin.site.register(Institution, InstitutionAdmin)

class PlanAdmin(admin.ModelAdmin):
	list_display = ('name', 'code', 'cost', 'value', 'duration')
	#fields = (('name', 'code'), 'content')
admin.site.register(Plan, PlanAdmin)


class AccountAdmin(admin.ModelAdmin):
	list_display = ('name', 'balance', 'expiry_date')
	#fields = (('name', 'code'), 'content')
admin.site.register(Account, AccountAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
	list_display = ('transaction_id', 'institution')
	#fields = (('name', 'code'), 'content')
admin.site.register(Subscription, SubscriptionAdmin)

