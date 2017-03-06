from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import get_object_or_404
import datetime
import uuid


# Create your models here.


class Plan(models.Model):
	name=models.CharField(max_length=250)
	code = models.CharField(max_length=10)
	cost = models.PositiveSmallIntegerField()
	value = models.PositiveSmallIntegerField()
	duration= models.PositiveSmallIntegerField()
	description = models.TextField(default='description goes here')

	def __str__(self):
		return self.name

class Account(models.Model):
	name = models.CharField(max_length=250)
	balance = models.PositiveSmallIntegerField(default=0)
	expiry_date = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return self.name

	def account_is_active(self):
		if self.expiry_date >= timezone.now() and self.balance > 0:
			return True
		


class Institution(models.Model):
	name = models.CharField(max_length=250)
	code = models.CharField(max_length=10)
	manager = models.OneToOneField(User, on_delete=models.CASCADE )
	account = models.ForeignKey(Account, blank=True, null=True)

	def __str__(self):
		return self.name

		
class Subscription(models.Model):
	transaction_id = models.UUIDField(default=uuid.uuid4, unique=True)
	institution = models.ForeignKey(Institution)
	plan = models.ForeignKey(Plan)
	time= models.DateTimeField(default=timezone.now)
	expiry_date = models.DateTimeField(default=timezone.now)
	balance = models.PositiveSmallIntegerField(default=0)	

	def __str__(self):
		return str(self.transaction_id)

	def new_expiry_date(self):
		data = get_object_or_404(Account, name=self.institution.name)
		self.expiry_date = data.expiry_date + datetime.timedelta(days=self.plan.duration*365)
		data.expiry_date = self.expiry_date
		data.save()
		return self.expiry_date

	def new_balance(self):
		data = get_object_or_404(Account, name=self.institution.name)
		self.balance = data.balance + self.plan.value
		data.balance = self.balance
		data.save()
		return self.balance

	def save(self, *args, **kwargs):
		self.expiry_date = self.new_expiry_date()
		self.new_balance()		
		super(Subscription, self).save(*args, **kwargs) # Call the "real" save() method.




