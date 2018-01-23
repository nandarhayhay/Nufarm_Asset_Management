from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.utils.dateformat import DateFormat
from NA_Models.models import goods
from django.core import serializers
from NA_DataLayer.common import CriteriaSearch
from NA_DataLayer.common import ResolveCriteria
from NA_DataLayer.common import StatusForm
#from NA_DataLayer.jqgrid import JqGrid
from django.conf import settings 
from NA_DataLayer.common import decorators
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import json
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django import forms
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponseRedirect
from distutils.util import strtobool
def NA_Goods(request):
	assert isinstance(request,HttpRequest)
	#buat nama-name column, key sama 
	populate_combo = []
	populate_combo.append({'label':'','columnName':'goods','dataType':'varchar'})
	populate_combo.append({'label':'date received','columnName':'datereceived','dataType':'datetime'})
	populate_combo.append({'label':'BrandName','columnName':'brandname','dataType':'varchar'})
	populate_combo.append({'label':'PricePerUnit','columnName':'priceperUnit','dataType':'decimal'})
	populate_combo.append({'label':'Depreciation_Method','columnName':'depreciationmethod','dataType':'char'})
	populate_combo.append({'label':'unit','columnName':'economiclife','dataType':'decimal'})
	populate_combo.append({'label':'Placement','columnName':'placement','dataType':'varchar'})
	return render(request,'app/MasterData/NA_F_Goods.html',{'populateColumn':populate_combo})