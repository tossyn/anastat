from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
import json

from .forms import *
from .models import * 

com_data = {}
tables = []

# Create your views here.
#@login_required
def sales(request):
	global com_data
	total_cost= 0
	form = UserRequestForm()
	alert_message =None
	#user=request.user
	if request.user.is_authenticated():		
		unpurchased_data = UserRequest.objects.filter(purchased=False, user=request.user)
		for data in unpurchased_data:
			total_cost += data.data_price
	else:
		unpurchased_data = None
		messages.info(request, 'Signin or signup if you do not have an existing account from the from the right side bar')
	# Populate the Left Side Bar with Components and Databases
	components = Component.objects.all()
	databases = []
	for com in components:
		c = Component.objects.get(name = com.name)
		databases.append(c.database_set.all())
	com_data = {component:database for component, database in zip(components, databases)}	
	# Handle POST Request from users
	if request.method == 'POST':	
		form = UserRequestForm(request.POST)
		if form.is_valid():
			if request.user.is_authenticated():	
				data = form.save(commit=False)
				data.user= request.user
				data.save()
				form.save_m2m() 
				#needed since using commit=False
				# You must save many2many values before you make use of them.
				# update_price() is a function defined in the UserRequest Model to calculate data price since zero is used as the default
				data.update_price()	
				data.save()			
				return redirect('sales')
			else:
				messages.warning(request, "Please Sign in or Sign up from the right side bar. Thank you.")
			
	return render(request, 'sales/data_new.html', {'com_data':com_data, 'form': form, 'unpurchased': unpurchased_data, 'total_cost':total_cost})


def ajax_table(request, pk):	
	database = get_object_or_404(Database, pk=pk)
	tables= database.table_set.all()
	t = serializers.serialize("json", tables)
	return HttpResponse(t, content_type='application/json')	

def ajax_level(request):
	pk = request.GET.get('pk', None)
	table = get_object_or_404(Table, pk=pk)
	levels = table.level_of_aggregation.all()
	l = serializers.serialize("json", levels)			
	return HttpResponse(l, content_type='application/json')
	
def ajax_freq(request):
	pk = request.GET.get('pk', None)
	table = get_object_or_404(Table, pk=pk)	
	freq = table.frequency.all()
	f = serializers.serialize("json", freq)		
	return HttpResponse(f, content_type='application/json')

def ajax_concat(request):
	table_pk = request.GET.get("pk1", None)
	table = get_object_or_404(Table, pk=table_pk)
	level_pk = request.GET.get("pk2", None)
	level = get_object_or_404(LevelOfAggregation, pk=level_pk)
	freq_pk = request.GET.get("pk3", None)
	freq = get_object_or_404(Frequency, pk=freq_pk)
	c = table.code+level.code+freq.code
	# concat1 is will return a single object
	concat1 =  get_object_or_404(ConcatTable, code=c)
	# concat2 will return a list like object
	concat2 = ConcatTable.objects.filter(code=c)
	concat = [concat1, concat2]
	return concat

def ajax_concat_price(request):
	con, concat = ajax_concat(request)	
	data = serializers.serialize("json", concat)
	return HttpResponse(data, content_type='application/json')
	

def ajax_vars(request):
	concat,con = ajax_concat(request)
	variables = concat.variable.all()
	data = serializers.serialize("json", variables)
	return HttpResponse(data, content_type='application/json')

def ajax_yrs(request):
	concat, con = ajax_concat(request)
	years= concat.avail_yrs.all()
	data = serializers.serialize("json", years)
	return HttpResponse(data, content_type='application/json')

def ajax_category(request):
	pk = request.GET.get('pk', None)
	level = get_object_or_404(LevelOfAggregation, pk=pk)	
	coa = level.category_of_aggregation.all()
	c = serializers.serialize("json", coa)		
	return HttpResponse(c, content_type='application/json')

# def user_data_req(request):
# 	if request.method == 'POST':
# 		form = UserRequestForm(request.POST)
# 		if form.is_valid():			
# 			data = form.save(commit=False)
# 			data.user= request.user
# 			data.save()
# 			return redirect('sales')
# 	else:
# 		form = UserRequestForm()
# 	return render(request, 'sales/data_new.html', {'form': form })

@login_required
def ajax_delete(request, pk):	
	data = get_object_or_404(UserRequest, pk=pk)
		
	if request.method =='POST':		
		data.delete()
		success_message = "Data successfully Removed"
		data = {'message':success_message}
		return redirect('sales')
		
	else:
		return render(request, 'sales/data_delete.html', {'pk':pk})

#Alternative login view for userlogin
def sales_login(request):
	username = request.POST['login']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request,user)
		return redirect('sales')
	else:
		return redirect('account_login')
