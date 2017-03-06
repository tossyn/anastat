from django.contrib import admin

# Register your models here.
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
	class Meta:
		model = Profile
	list_display = ('user', 'sex', 'phone_number', 'city', 'affiliate_membership', 'institution', 'is_manager','membership_approved')

admin.site.register(Profile, ProfileAdmin)