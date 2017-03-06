"""storefront URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    # url from the main sales page
    url(r'^affiliate/manager/$', views.affiliate_manager, name='affiliate_manager'),
    url(r'^affiliate/manager/approve/transaction/(?P<pk>[0-9]+)$', views.approve_transaction, name='approve_transaction'),
    url(r'^affiliate/manager/disapprove/transaction/(?P<pk>[0-9]+)$', views.disapprove_transaction, name='disapprove_transaction'),
    url(r'^affiliate/manager/approve/membership/(?P<pk>[0-9]+)$', views.approve_membership, name='approve_membership'),
    url(r'^affiliate/manager/disapprove/membership/(?P<pk>[0-9]+)$', views.disapprove_membership, name='disapprove_membership'),

]
