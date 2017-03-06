from django import forms

from django.contrib.auth.models import User
from profiles.models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('sex', 'phone_number', 'address',
        	'city',
        	'state',
        	'country',
        	'affiliate_membership',
        	'institution',
            'institution_code',
        	'membership_code')
        widgets ={
        'institution_code':forms.PasswordInput()
        }

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        affiliate_membership = cleaned_data.get("affiliate_membership")
        institution = cleaned_data.get("institution")
        institution_code = cleaned_data.get("institution_code")
        membership_code = cleaned_data.get("membership_code")

        if affiliate_membership == True:
            if institution and institution_code and membership_code:
                # check if the code matches the code of the selected institution
                if institution_code != institution.code:
                    raise forms.ValidationError("Invalid code for %s." %(institution))
                
            else:
                raise forms.ValidationError(" Institution, Institution code and Membership code are all required for affiliate membership")
        return cleaned_data
