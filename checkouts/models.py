from __future__ import unicode_literals
import uuid
import datetime
from django.conf import settings

from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib import messages

from sales.models import UserRequest
from affiliates.models import *

# Create your models here.
class Checkout(models.Model):
	PAYMENT_CHOICES = (
		('BP', 'Bank Payment'),
		('AP', 'Affiliate Privilege'),
		#('MT', 'Mobile Transfer'),
		#('BP', 'Bank Payment'),
    	#('IB', 'Internet Banking'),
    	#('CC', 'Credit Card'),    
	)

	transaction_id = models.UUIDField(default=uuid.uuid4, unique=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	data_requests=models.ManyToManyField(UserRequest)
	data_cost = models.IntegerField(default=0)
	cost_with_vats =  models.IntegerField(default=0)
	time= models.DateTimeField(default=timezone.now)
	payment_mode=models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default= 'BP'
    	)
	institution = models.ForeignKey(Institution, null=True, blank=True)
	institution_code = models.CharField(max_length=25, null =True, blank=True)
	payment_confirmed = models.BooleanField(default=False)
	affiliate_manager_approved = models.NullBooleanField(blank=True, null=True)
	approved_time= models.DateTimeField(blank=True, null=True)
	data_delivered = models.BooleanField(default=False)

	def __str__(self):
		return str(self.transaction_id)

	def limit_user_request(self):
		return {'user_request_limit':UserRequest.objects.filter(user=self.user, purchased=False)}

	def is_affiliated(self):
		return self.institution_code == Institution.code

	def deplete_account(self, request):
		data = get_object_or_404(Account, name = self.institution)
		if data.account_is_active():
			if data.balance >= self.cost_with_vats:
				data.balance -= self.cost_with_vats
				data.save()
				return data.balance
			else:
				messages.warning(request, 'Subscription balance is not sufficient for the proposed transaction.')
		else:
			messages.error(request, 'Subscription has depleted or expired')


	def approve_transaction(self):
		self.affiliate_manager_approved = True
		return self.affiliate_manager_approved

	def disapprove_transaction(self):
		self.affiliate_manager_approved = False
		return self.affiliate_manager_approved
	def set_approved_time(self):
		self.approved_time = timezone.now()
		return self.approved_time
	class Meta:
		permissions=(("can_approve_transaction", "Approve transaction approval request sent to affiliate manager"), ("can_disapprove_transaction", "Disapprove transaction apprroval request  sent to affiliate manager"),)


	

	

	



	



