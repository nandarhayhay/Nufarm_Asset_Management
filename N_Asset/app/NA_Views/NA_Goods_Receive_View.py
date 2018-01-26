from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.utils.dateformat import DateFormat
from NA_Models.models import NAGoodsReceive
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
def NA_Goods_Receive(request):
	assert isinstance(request,HttpRequest)
	#buat nama-name column, key sama 
	populate_combo = []
	populate_combo.append({'label':'Goods Descriptions','columnName':'goods','dataType':'varchar'})
	populate_combo.append({'label':'Date Received','columnName':'datereceived','dataType':'datetime'})
	populate_combo.append({'label':'Suplier Name','columnName':'suplier','dataType':'varchar'})
	populate_combo.append({'label':'Received By','columnName':'received_by','dataType':'varchar'})
	populate_combo.append({'label':'PR By','columnName':'pr_by','dataType':'varchar'})
	populate_combo.append({'label':'Total Purchased','columnName':'totalpurchased','dataType':'int'})
	populate_combo.append({'label':'Total Received','columnName':'totalreceived','dataType':'int'})
	return render(request,'app/Transactions/NA_F_Goods_Receive.html',{'populateColumn':populate_combo})
def NA_Goods_Receive_Search(request):
	IcolumnName = request.GET.get('columnName');
	IvalueKey =  request.GET.get('valueKey')
	IdataType =  request.GET.get('dataType')
	Icriteria =  request.GET.get('criteria')
	Ilimit = request.GET.get('rows', '')
	Isidx = request.GET.get('sidx', '')
	Isord = request.GET.get('sord', '')
	if(',' in Isidx):
		Isidx = Isidx.split(',')

	criteria = ResolveCriteria.getCriteriaSearch(str(Icriteria))
	dataType = ResolveCriteria.getDataType(str(IdataType))
	if(Isord is not None and str(Isord) != ''):
		NAData = NAGoodsReceive.objects.PopulateQuery(IcolumnName,IvalueKey,criteria,dataType)
	else:
		NAData = NAGoodsReceive.objects.PopulateQuery(IcolumnName,IvalueKey,criteria,dataType)
	
	totalRecord = NAData.count()
	paginator = Paginator(NAData, int(Ilimit)) 
	try:
		page = request.GET.get('page', '1')
	except ValueError:
		page = 1
	try:
		dataRows = paginator.page(page)
	except (EmptyPage, InvalidPage):
		dataRows = paginator.page(paginator.num_pages)
		
	rows = []
	#column IDapp 	goods 	datereceived supliername FK_ReceivedBy 	Received_By FK_P_R_By pr_by totalpurchased totalreceived 
	i = 0;
	for row in dataRows.object_list:
		datarow = {"id" :row['idapp'], "cell" :[i+1,row['goods'],row['datereceived'],row['supliername'],row['FK_ReceivedBy'],row['Received_By'],row['FK_P_R_By'], \
			row['pr_by'],row['totalpurchased'],row['totalreceived'],row['inactive'],datetime.date(row['CreatedDate']),row['CreatedBy']]}
		#datarow = {"id" :row.idapp, "cell" :[row.idapp,row.itemcode,row.goodsname,row.brandname,row.unit,row.priceperunit, \
		#	row.placement,row.depreciationmethod,row.economiclife,row.createddate,row.createdby]}
		rows.append(datarow)
	results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
	return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')	