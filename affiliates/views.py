from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse

from .models import *
from checkouts.models import Checkout
from profiles.models import Profile

# Create your views here.

@login_required
# @permission_required('checkout.can_approve_transaction', raise_exception=True)
# @permission_required('checkout.can_disapprove_transaction', raise_exception=True)
def affiliate_manager(request):
	#user=get_object_or_404(User, pk=pk)
	if request.user.is_authenticated():
		user = request.user
		if user.profile.is_manager:
			institution = get_object_or_404(Institution, manager=user)
			data = Checkout.objects.filter(institution=institution)
			data_yet_to_approve =data.filter(affiliate_manager_approved = None, payment_mode = 'AP').order_by("time")
			data_approved = data.filter(affiliate_manager_approved = True, payment_mode = 'AP')
			data1 = Profile.objects.filter(institution=institution).filter(membership_approved=None)
						
			return render(request, 'affiliates/managers.html', {'data':data_yet_to_approve, 'data_approved': data_approved, 'data1':data1, 'institution':institution } )
		messages.error = (request, 'You are not authorized to visit that page keep off.')
		data = "<h1>Access Denied</h1><p><a href='/sales/'>Back to Sales page</a></p>"
	#return redirect('sales')
	return HttpResponse(data) 

@login_required
# @permission_required('checkout.can_approve_transaction', raise_exception=True)
def approve_transaction(request, pk):
	if request.user.profile.is_manager:
		data = get_object_or_404(Checkout, pk=pk)
		if request.method =='POST':
			if data.deplete_account(request):# Method from affiliate.Account Model
				data.approve_transaction()
				data.set_approved_time()
				data.save()
				messages.success(request, 'Transaction Approved')
			return redirect('affiliate_manager')
		else:
			return render(request, 'affiliates/approve_transaction.html', {'pk':pk})
	else:
		messages.error = (request, 'You are not authorized to visit that page keep off.')
		data = "<h1>Access Denied</h1><p><a href='/sales/'>Back to Sales page</a></p>"
		return HttpResponse(data)
	
@login_required
# @permission_required('checkout.can_disapprove_transaction', raise_exception=True)
def disapprove_transaction(request, pk):
	if request.user.profile.is_manager:
		data = get_object_or_404(Checkout, pk=pk)
		if request.method =='POST':
			data.disapprove_transaction()
			data.save()
			messages.warning(request, 'Transaction Disapproved')
			return redirect('affiliate_manager')
		else:
			return render(request, 'affiliates/disapprove_transaction.html', {'pk':pk})
	else:
		messages.error = (request, 'You are not authorized to visit that page keep off.')
		data = "<h1>Access Denied</h1><p><a href='/sales/'>Back to Sales page</a></p>"
		return HttpResponse(data)

@login_required
# @permission_required('checkout.can_approve_transaction', raise_exception=True)
def approve_membership(request, pk):
	if request.user.profile.is_manager:
		user = get_object_or_404(User, pk=pk)
		if request.method =='POST':			
			user.profile.membership_approved=True		
			user.save()
			messages.success(request, 'Membership Approved')
			return redirect('affiliate_manager')
		else:
			return render(request, 'affiliates/approve_membership.html', {'pk':pk})
	else:
		messages.error = (request, 'You are not authorized to visit that page keep off.')
		data = "<h1>Access Denied</h1><p><a href='/sales/'>Back to Sales page</a></p>"
		return HttpResponse(data)
	
@login_required
# @permission_required('checkout.can_disapprove_transaction', raise_exception=True)
def disapprove_membership(request, pk):
	if request.user.profile.is_manager:
		user = get_object_or_404(User, pk=pk)
		if request.method =='POST':
			user.profile.membership_approved=False			
			user.save()
			messages.warning(request, 'Membership Denied')
			return redirect('affiliate_manager')
		else:
			return render(request, 'affiliates/disapprove_membership.html', {'pk':pk})
	else:
		messages.error = (request, 'You are not authorized to visit that page keep off.')
		data = "<h1>Access Denied</h1><p><a href='/sales/'>Back to Sales page</a></p>"
		return HttpResponse(data)

