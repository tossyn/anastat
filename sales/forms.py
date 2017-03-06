from django import forms

from sales.models import *
from multiselectfield import MultiSelectField
class UserRequestForm(forms.ModelForm):
	class Meta:
		model = UserRequest
		fields = ('table', 'level_of_aggregation', 'frequency', 'categories_of_aggregation', 'variables', 'years', 'comment')
		widgets ={
		'table':forms.Select(),
		'level_of_aggregation':forms.Select(),
		'frequency':forms.Select(),
		'categories_of_aggregation': forms.SelectMultiple(),
		'variables': forms.SelectMultiple(),
		'years': forms.SelectMultiple()

		}

		# table = forms.ModelChoiceField(queryset= Table.objects.filter(pk=1))
		# level_of_aggregation = forms.ModelChoiceField(queryset=Table.objects.filter(pk=1).level_of_aggregation.all())
		# frequency = forms.ModelChoiceField(queryset=Table.objects.filter(pk=1).frequency.all())
		# categories_of_aggregation = forms.ModelMultipleChoiceField(queryset=LevelOfAggregation.objects.filter(pk=1).category_of_aggregation.all())
		# variables = forms.ModelMultipleChoiceField(queryset=ConcatTable.objects.filter(pk=5).variable.all())
		# years = forms.ModelMultipleChoiceField(queryset=ConcatTable.objects.filter(pk=5).avail_yrs.all())


		# class Meta:
		# 	model = UserRequest
		# 	fields = ('table', 'level_of_aggregation', 'frequency', 'categories_of_aggregation', 'variables', 'years', 'comment')
