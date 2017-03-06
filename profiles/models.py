from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from affiliates.models import *

# Create your models here.

class Profile(models.Model):
	SEX = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	sex = models.CharField(max_length=6, choices = SEX)
	phone_number = PhoneNumberField(help_text="phone number in this format +2348076222307")
	address = models.CharField(max_length=200, blank=True)
	city = models.CharField(max_length=70, blank=True)
	state = models.CharField(max_length=70, blank=True)
	country = models.CharField(max_length=70, blank=True)
	affiliate_membership =  models.BooleanField(default=False, help_text="FOR CLIENT AFFILIATED TO SUBSCRIBING INSTITUTION")
	institution = models.ForeignKey(Institution, null=True, blank=True)
	membership_code = models.CharField(max_length=25, null =True, blank=True, help_text="Matric Number or Identification Number issued by your institution")
	institution_code = models.CharField(max_length=25, null =True, blank=True)
	is_manager = models.BooleanField(default=False, help_text="Check for affiliate managers")

	membership_approved=models.NullBooleanField(blank=True, null=True)
	

	def __str__(self):
	    return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()