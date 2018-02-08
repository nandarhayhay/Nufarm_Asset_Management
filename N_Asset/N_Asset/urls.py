"""
Definition of urls for N_Asset.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
from app.NA_Views import NA_Goods_View,NA_Goods_Receive_View
import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

	#View the Goods
	url(r'^NA_Goods/$',NA_Goods_View.NA_Goods,name='GoodMaster'),
	url(r'^NA_Goods/NA_Goods_Search/$',NA_Goods_View.NA_Goods_Search,name='searchGoods'),
	url(r'^NA_Goods/SearchBrand/$',NA_Goods_View.Search_Brand, name='SearchBrand'),
    url(r'^NA_Goods/ShowEntry',NA_Goods_View.ShowEntry,name='ShowEntry'),
	url(r'^NA_Goods/customFilter',NA_Goods_View.ShowCustomFilter,name='ShowCustomFilter'),
	url(r'^NA_Goods/Delete/$',NA_Goods_View.deleteItem,name='DeleteGoods'),
	url(r'^NA_Goods/setInActive/$',NA_Goods_View.setInActive,name='SetInActive'),

	#view the goods_receive
		url(r'^NA_Goods_Receive/$',NA_Goods_Receive_View.NA_Goods_Receive,name='GoodsReceive'),
		url(r'^NA_Goods_Receive/ShowEntry_Receive',NA_Goods_Receive_View.ShowEntry_Receive,name='ShowEntryReceivey'),
		url(r'^NA_Goods_Receive/getGoods/$',NA_Goods_Receive_View.getGoods,name='getGoods'),
		url(r'^NA_Goods_Receive/Delete/$',NA_Goods_Receive_View.Delete,name='delete'),
		url(r'^NA_Goods_Receive/HasExists/$',NA_Goods_Receive_View.HasExists,name='HasExists'),
		url(r'^NA_Goods_Receive/getSuplier/$',NA_Goods_Receive_View.getSuplier,name='getSuplier'),
		url(r'^NA_Goods_Receive/getEmployee/$',NA_Goods_Receive_View.getEmployee,name='getEmployee'),
		url(r'^NA_Goods_Receive/SearchGoodsbyForm/$',NA_Goods_Receive_View.SearchGoodsbyForm,name='SearchGoodsbyForm'),
		url(r'^NA_Goods_Receive/SearchSuplierbyForm/$',NA_Goods_Receive_View.SearchSuplierbyForm,name='SearchSuplierbyForm'),
		url(r'^NA_Goods_Receive/SearchEmployeebyform/$',NA_Goods_Receive_View.SearchEmployeebyform,name='SearchEmployeebyform'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
