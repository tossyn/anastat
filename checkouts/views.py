from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django.core.mail import send_mail, send_mass_mail
from django.utils.translation import gettext as _
from django.conf import settings
import json

#from .forms import *
from .models import *
from sales.models import UserRequest
from checkouts.forms import *

# Create your views here.
@login_required
def checkout(request):
	data = UserRequest.objects.filter(purchased=False, user=request.user)
	if len(data)==0:
		return redirect('sales')
	data_cost = 0
	for item in  data:
		data_cost+=item.data_price
	cost_with_vats = data_cost*1.05

	form=CheckoutForm()
	if request.method == 'POST':
	# 	if request.POST['payment_mode']=='AP':
			
		form =CheckoutForm(request.POST)		

		if form.is_valid():
			#form.clean()
			transaction = form.save(commit=False)
			transaction.user= request.user
			# Check if user is an affiliate member or not to prevent them from using the privilege
			if transaction.payment_mode =='AP':
				if transaction.user.profile.membership_approved== False or transaction.user.profile.membership_approved== None:
					form.add_error('institution', 'You are not registered as an affiliate member to any institution or your membership claim is disapproved. Consider another payment option')
					return render(request, 'checkouts/checkout.html', {'data':data, 'cost':data_cost, 'cost_with_vats':cost_with_vats, 'form':form })
				if transaction.institution != transaction.user.profile.institution:
					form.add_error('institution', 'You are not registered as an affiliate member to %s. Use your institution or consider another payment option.' %(transaction.institution))
					return render(request, 'checkouts/checkout.html', {'data':data, 'cost':data_cost, 'cost_with_vats':cost_with_vats, 'form':form })
			
			transaction.save()						
			transaction.data_requests=data
			# calculate the total cost of data and assign it to data cost
			for item in data:
				item.set_purchased() #modify UserRequest Object.purchased to True using set_purchased() method in UserRequest in sales models.
				item.save()# save the instance
				transaction.data_cost+=item.data_price
			# calculate cost with 5% vat 
			transaction.cost_with_vats = transaction.data_cost*1.05
			#data1 = UserRequest.objects.filter(purchased=False, user=request.user)
			#transaction.data_requests=data
			transaction.save()
		
			alert_message='Successful Checkout! Please make your payment as indicated to ensure prompt delivery of data. Thank you for your patronage'
			banker= "GTBank"
			account_num='0000000000'
			sales_rep='Dammy: +2348000000000'
			subject= "Request Order from %s -  %s."%(request.user.username, request.user.profile.phone_number )
			emailFrom = request.user.email
			emailTo = ['tossynfaw@gmail.com', request.user.email] #"oluwatosinfawibe@gmail.com"
			#mail=[] 			
			for item in data:
				message = """
		Use DATABASENAME			%s
                Select VARIABLENAMES			%s
                From TABLENAME					%s
                Where CONDITIONS				%s
                Where CONDITIONS 				%s
                """ %(item.table.database, item.display_variables(), item.code, item.display_categories_of_aggregation(), item.display_years())
				send_mail(subject, message, emailFrom, emailTo)
				#mail += (subject, message, emailFrom, emailTo)
			#send_mass_mail(mail,fail_silently=False)
			if transaction.payment_mode =='AP': 
				subject =" Transaction Approval"
				message = """Dear %s,
                A transaction approval request has been sent to you for approval from %s %s with identification number %s. Thanks for prompt attention! 
                AnaStat SYSTEM """ %(request.user.profile.institution.manager,request.user.first_name, request.user.last_name, request.user.profile.membership_code)
				emailFrom = request.user.email
				emailTo = [request.user.profile.institution.manager.email] #"oluwatosinfawibe@gmail.com" 
				send_mail(subject, message, emailFrom, emailTo)
			messages.success(request, _('Thanks for your patronage. One of our customer representatives with contact you shortly.'))

			return render(request, 'checkouts/checkout.html', {'data':data, 'alert':alert_message, 'bank':banker, 'account':account_num, 'sales_rep':sales_rep, 'transaction': transaction, 'message':message })

	return render(request, 'checkouts/checkout.html', {'data':data, 'cost':data_cost, 'cost_with_vats':cost_with_vats, 'form':form })



		

