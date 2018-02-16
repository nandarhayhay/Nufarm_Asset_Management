﻿"""
Definition of urls for N_Asset.
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from app.NA_Views import NA_Goods_View, NA_User_View, NA_Employee_View, NA_LogEvent_View, NA_Suplier_View, NA_EmailData_View, NA_Acc_Fa_View
import app.views
# Uncomment the next lines to enable the admin:
# admin.autodiscover()
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),

    #User's URL
    url(r'^login/$', NA_User_View.login_view, name='login'),
    url(r'^register/$', NA_User_View.NA_User_Register, name='register'),
    url(r'^profile/(?P<username>\w+)/edit/$', NA_User_View.user_profile, name='user_profile'),
    url(r'^logout/$', NA_User_View.logout_view, name='logout'),

    #NA_Employee
    url(r'^NA_Employee/$', NA_Employee_View.NA_Employee, name='NA_Employee'),
    url(r'^NA_Employee/delete/$', NA_Employee_View.NA_Employee_delete, name='NA_Employee_delete'),
    url(r'^NA_Employee/EntryEmployee/$', NA_Employee_View.EntryEmployee),
    url(r'^NA_Employee/customFilter/$', NA_Employee_View.ShowCustomFilter),
    url(r'^NA_Employee/getData/$', NA_Employee_View.NA_EmployeeGetData),

    #NA_Suplier
    url(r'^NA_Suplier/$', NA_Suplier_View.NA_Suplier, name='NA_Suplier'),
    url(r'^NA_Suplier/delete/$', NA_Suplier_View.NA_Suplier_delete, name='NA_Suplier_delete'),
    url(r'^NA_Suplier/EntrySuplier/$', NA_Suplier_View.EntrySuplier),
    url(r'^NA_Suplier/getData/', NA_Suplier_View.NA_SuplierGetData),
    url(r'^NA_Suplier/customFilter/$', NA_Suplier_View.ShowCustomFilter),

    #NA_EmailData
    url(r'^NA_EmailData/$', NA_EmailData_View.NA_EmailData, name='NA_EmailData'),
    url(r'^NA_EmailUplData/$', NA_EmailData_View.NA_EmailUplData, name='NA_EmailUplData'),
    url(r'^NA_EmailData/searchBiodata/$', NA_EmailData_View.searchBiodata, name='NA_EmailData_searchBiodata'),
    url(r'^NA_Email/retriveBio/$', NA_EmailData_View.NA_Email_retriveBio, name='NA_Email_retriveBio'),

    #Log Event
    url(r'^NA_LogEvent/$', NA_LogEvent_View.NA_LogEvent_data),
    url(r'^NA_LogEvent/desc/$', NA_LogEvent_View.LogDescriptions, name='LogDescriptions'),

	#View the Goods
	url(r'^NA_Goods/$',NA_Goods_View.NA_Goods,name='GoodMaster'),
	url(r'^NA_Goods/NA_Goods_Search/$',NA_Goods_View.NA_Goods_Search,name='searchGoods'),
	url(r'^NA_Goods/SearchBrand/$',NA_Goods_View.Search_Brand, name='SearchBrand'),
    url(r'^NA_Goods/ShowEntry',NA_Goods_View.ShowEntry,name='ShowEntry'),
	url(r'^NA_Goods/customFilter',NA_Goods_View.ShowCustomFilter,name='ShowCustomFilter'),
	url(r'^NA_Goods/Delete/$',csrf_exempt(NA_Goods_View.deleteItem),name='DeleteGoods'),
	url(r'^NA_Goods/setInActive/$',NA_Goods_View.setInActive,name='SetInActive'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	#NA Acc FA
	url(r'^NA_Acc_FA/$',NA_Acc_Fa_View.NA_Acc_FA, name='NA_Acc'),
	url(r'^NA_Acc_FA/ShowEntry/$',NA_Acc_Fa_View.EntryAcc, name='NA_Acc_Entry'),
    url(r'NA_Acc_FA/getData/$',NA_Acc_Fa_View.NA_AccGetData),
    url(r'NA_Acc_FA/SearchGoods/$',NA_Acc_Fa_View.searchGoods),
	url(r'^NA_Acc_FA/getGoods/$',NA_Acc_Fa_View.getGoods_data),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
]

# untuk akses url media(picture) hasil upload User
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]