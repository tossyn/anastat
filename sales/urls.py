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
    url(r'^sales/$', views.sales, name='sales'),
    # url for table
    url(r'^sales/table/(?P<pk>[0-9]+)$', views.ajax_table, name='sales_table'),
    
    # call to ajax to render options for levels of aggregation and frequencies
    url(r'^sales/data/level/$', views.ajax_level, name='sales_level'),
    url(r'^sales/data/freq/$', views.ajax_freq, name='sales_freq'),
    url(r'^sales/data/category/$', views.ajax_category, name='sales_category'),
    url(r'^sales/data/vars/$', views.ajax_vars, name='sales_vars'),
    url(r'^sales/data/years/$', views.ajax_yrs, name='sales_years'),
    url(r'^sales/data/concat_price/$', views.ajax_concat_price, name='sales_concat_price'),

    url(r'^sales/delete/(?P<pk>[0-9]+)$', views.ajax_delete, name='sales_data_delete'),
    url(r'^sales/login$', views.sales_login, name='sales_login'),
    # url for table
]
