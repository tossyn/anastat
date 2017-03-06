from django import forms

from django.contrib.auth.models import User
from profiles.models import Profile
from checkouts.models import Checkout
from affiliates.models import Institution

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ('payment_mode', 'institution', 'institution_code')
        widgets ={
		'institution_code':forms.PasswordInput()
		}

    def clean(self):
    	cleaned_data = super(CheckoutForm, self).clean()
    	payment_mode = cleaned_data.get("payment_mode")
    	institution = cleaned_data.get("institution")
    	institution_code = cleaned_data.get("institution_code")    	
    	if payment_mode == 'AP':
    		if institution and institution_code:
    			# check if the code matches the code of the selected institution
    			if institution_code != institution.code:
    				raise forms.ValidationError("Invalid code for %s. Please contact your institution's affiliate manager or select another mode of payment" %(institution))
                
    		else:
    			raise forms.ValidationError(" Both institution and code are required for affiliate privilege")
    	return cleaned_data
