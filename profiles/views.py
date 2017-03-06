from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect

from allauth.account.forms import SignupForm
from allauth.account.utils import complete_signup
from formtools.wizard.views import SessionWizardView
from formtools.preview import FormPreview

from .models import *
from .forms import *
from checkouts.models import Checkout

# Create your views here.
def home(request):
	context = {}
	template = 'home.html'
	return render(request, template, context)
def about(request):
	context = {}
	template = 'about.html'
	return render(request, template, context)
@login_required
def user_profile(request):
	user = request.user
	context = {'user': user}
	template = 'profile.html'
	return render(request, template, context)


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # get the instance of the new user
            user = get_object_or_404(User, pk=request.user.pk)
            if user.profile.affiliate_membership==True and user.profile.membership_approved == None:
                subject =" Membership Approval"
                message = """Dear %s,
                A membership approval request has been sent to you for approval from %s %s with identification number %s. Thanks for prompt attention! 
                AnaStat SYSTEM """ %(user.profile.institution.manager,user.first_name, user.last_name, user.profile.membership_code)
                emailFrom = user.email
                emailTo = [user.profile.institution.manager.email] #"oluwatosinfawibe@gmail.com" 
                send_mail(subject, message, emailFrom, emailTo)
                messages.success(request, _('Your profile was successfully updated and an approval mail has been sent to your instition for confirmation of your membership. Thanks '))

            else:
                messages.success(request, _('Your profile was successfully updated!'))

            return redirect('sales')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        previous_tranactions = Checkout.objects.filter(user=request.user)
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form, 'pre_trans':previous_tranactions
    })



class ProfileFormPreview(FormPreview):

    def done(self, request, cleaned_data):
        # Do something with the cleaned_data, then redirect
        # to a "success" page.
        
        update_profile(request)
        return HttpResponseRedirect('/sales/')



class Wizard(SessionWizardView):
    
    template_name = 'registration_wizard_form.html'

    def done(self, form_list, **kwargs):
    	for form in form_list:
    		if isinstance(form, SignupForm):
    			user = form.save(self.request)
    			complete_signup(self.request, user, settings.ACCOUNT_EMAIL_VERIFICATION, settings.LOGIN_REDIRECT_URL)
    		else:
    			update_profile(request)

    	return render_to_response('done.html', {'form_data': [form.cleaned_data for form in form_list],})
