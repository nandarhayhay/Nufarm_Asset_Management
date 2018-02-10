from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.utils.dateformat import DateFormat
from NA_Models.models import NAGoodsReceive, goods,NASuplier,Employee
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
	populate_combo.append({'label':'Received By','columnName':'receivedby','dataType':'varchar'})
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
		NAData = NAGoodsReceive.objects.PopulateQuery(IcolumnName,IvalueKey,criteria,dataType).order_by('-' + str(Isidx))
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
	#column IDapp 	goods 	datereceived supliername FK_ReceivedBy 	receivedby FK_P_R_By pr_by totalpurchased totalreceived 
	i = 0;
	for row in dataRows.object_list:
		datarow = {"id" :row['idapp'], "cell" :[i+1,row['goods'],row['datereceived'],row['supliername'],row['FK_ReceivedBy'],row['receivedby'],row['FK_P_R_By'], \
			row['pr_by'],row['totalpurchased'],row['totalreceived'],row['inactive'],datetime.date(row['CreatedDate']),row['CreatedBy']]}
		#datarow = {"id" :row.idapp, "cell" :[row.idapp,row.itemcode,row.goodsname,row.brandname,row.unit,row.priceperunit, \
		#	row.placement,row.depreciationmethod,row.economiclife,row.createddate,row.createdby]}
		rows.append(datarow)
	results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
	return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
	
def getCurrentDataModel(request,form):	#fk_goods, datereceived, fk_suplier, totalpurchase, totalreceived,  fk_receivedby fk_p_r_by, idapp_fk_goods, idapp_fk_p_r_by, idapp_fk_receivedby,descriptions
	return {'idapp_fk_goods':form.cleaned_data['idapp_fk_goods'],'fk_goods':form.cleaned_data['fk_goods'],'datereceived':form.cleaned_data['datereceived'],'fk_suplier':form.cleaned_data['fk_suplier'],
		 'totalpurchase':form.cleaned_data['totalpurchase'],'totalreceived':form.cleaned_data['totalreceived'],'fk_receivedby':form.cleaned_data['fk_receivedby'],'idapp_fk_p_r_by':form.cleaned_data['idapp_fk_p_r_by'],'hasRefData':form.cleaned_data['hasRefData'],
		 'idapp_fk_receivedby':form.cleaned_data['idapp_fk_receivedby'],'descriptions':form.cleaned_data['descriptions'],'createddate':str(datetime.now().date()),'createdby':request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin' }
def HasExists(request):
	FK_goods = request.POST.get('fk_goods')
	totalpurchase = request.POST.get('totalpurchase')
	datereceived = request.POST.get('datereceived')
	if NAGoodsReceive.objects.hasExists(FK_goods,datereceived,totalpurchase):
		result = 'success'
		statuscode = 200
	return HttpResponse(json.dumps({'message':'Data has exists\nAre you sure you want to add the same data ?'}),status = statuscode, content_type='application/json')
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")
@ensure_csrf_cookie
def ShowEntry_Receive(request):
	authentication_classes = []
	status = 'Add'
	initializationForm={}
	statuscode = 200
	data = None
	if request.POST:
		data = request.body
		data = json.loads(data)
		status = data['status']
	else:
		status = 'Add' if request.GET.get('status') == None else request.GET.get('status')	
		#set initilization
	if status == 'Add':		
		if request.POST:
			form = NA_Goods_Receive_Form(data)
			statuscode = 200
			if form.is_valid():
				#save data
				#ALTER TABLE n_a_goods MODIFY IDApp INT AUTO_INCREMENT PRIMARY KEY
				form.clean()					
				data = getCurrentDataModel(request,form)	
				#check if exists the same data to prevent users double input,parameter data to check FK_goods,datereceived,totalpurchase				
				result = NAGoodsReceive.objects.SaveData(data,StatusForm.Input)
				if result != 'success':
					statuscode = 500
				return HttpResponse(json.dumps({'message':result}),status = statuscode, content_type='application/json')
			else: 
				return HttpResponse(json.dumps({'message':'invalid form data'}),status = 400, content_type='application/json')
		else:				
			form = NA_Goods_Receive_Form(initial=initializationForm)
			form.fields['status'].widget.attrs = {'value':status}	
			form.fields['hasRefData'].widget.attrs = {'value': False}
			return render(request, 'app/Transactions/Goods_Receive.html', {'form' : form})
	elif status == 'Edit' or status == "Open":	
		hasRefData = NAGoodsReceive.objects.hasReference({FK_goods:reques.GET.get('idapp_fk_goods'), DateReceived:reques.GET.get('DateReceived')},False)	
		if request.POST:

			form = NA_Goods_Receive_Form(data)
			if form.is_valid():
				form.clean()
				#save data
				data = getCurrentDataModel(request,form);
				data.update(IDApp=data['idapp'])
				data.update(hasRefData=hasRefData)
				result = NAGoodsReceive.objects.SaveData(data,StatusForm.Edit)
				if result != 'success':
					statuscode = 500
				return HttpResponse(json.dumps({'message':result}),status = statuscode, content_type='application/json')
				#check itemCode
				#if scorm.objects.filter(Header__id=qp.id).exists()				
				#return HttpResponse('success', 'text/plain')
		else:
			#get data from database
			IDApp = reques.GET.get('IDApp')
			#Ndata = goods.objects.getData(IDApp)[0]
			Ndata = NAGoodsReceive.objects.getData(IDApp)[0]	
			#idapp,fk_goods, idapp_fk_goods,datereceived, fk_suplier,supliername, totalpurchase, totalreceived, idapp_fk_received, fk_receivedby,employee_received,idapp_fk_p_r_by, fk_p_r_by,employee_pr, descriptions	
			NAData = {'idapp':IDApp,'idapp_fk_goods':Ndata.idapp_fk_goods,'fk_goods':Ndata.fk_goods,'goods_desc':Ndata.goods,'datereceived':Ndata.datereceived,'fk_suplier':Ndata.fk_suplier,'supliername':Ndata.supliername,
					'totalpurchase':Ndata.totalpurchase,'totalreceived':Ndata.totalreceived,'idapp_fk_received':Ndata.idapp_fk_received,'fk_receivedby':Ndata.fk_receivedby,'employee_received':Ndata.employee_received,
					'idapp_fk_p_r_by':Ndata.idapp_fk_p_r_by,'fk_p_r_by':Ndata.idapp_fk_p_r_by,'employee_pr':Ndata.employee_pr,'descriptions':Ndata.descriptions}
			NAData.update(initializeForm=json.dumps(NAData,cls=DjangoJSONEncoder)) 
			form = NA_Goods_Receive_Form(data=NAData)
			form.fields['status'].widget.attrs = {'value':status}
			if hasRefData:
				form.fields['totalreceived'].disabled = True
			form.fields['hasRefData'].widget.attrs = {'value': str2bool(hasRefData)} 
			return render(request, 'app/Transactions/Goods_Receive.html', {'form' : form})
def Delete(request):
	try:
		#result=NAGoodsReceive.objects.delete(
		IDApp = request.POST.get('idapp')
		Ndata = NAGoodsReceive.objects.getData(IDApp)[0]
		NAData = {'idapp':IDApp,'idapp_fk_goods':Ndata.idapp_fk_goods,'datereceived':Ndata.datereceived}
		result = NAGoodsReceive.objects.delete(Data)
		return HttpResponse(json.dumps(result,cls=DjangoJSONEncoder),status = 200, content_type='application/json') 
	except :
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
def getGoods(request):
	"""get goods by itemcode return 'goodsname' + 'brandname' + 'itemcode' as goods criteria = iexact
	"""

	result={};
	try:
		itemcode = request.GET.get('itemcode')
		result = goods.customs.getGoods(itemcode)
		if len(list(result)):
			result = result[0]
			result = {'goods':result.goods}
		else:
			result = {'goods':''}
		return HttpResponse(json.dumps(result,cls=DjangoJSONEncoder),status = 200, content_type='application/json') 
	except Exception as e:					
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
def getSuplier(request):
	"""get supliername by supliercode return supliername criteria = ixact'
	"""
	result={}
	try:
		supliercode = request.GET.get('supliercode')
		result = NASuplier.customManager.getSuplier(supliercode)
		if len(list(result)):
			result = result[0]
		else :
			result={}
		return HttpResponse(json.dumps(result,cls=DjangoJSONEncoder),status = 200, content_type='application/json') 
	except Exception as e:					
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
def getEmployee(request):
	"""get employee name by nik return employee name criteria = iexact"""
	nik =  request.GET.get('nik')
	result={};
	result = Employee.customManager.getEmployee(nik)
	if len(list(result)):
		result = result[0]
	else :
		result={}
	#if result.count > 0:
	#	result = result[0]	
		#for brandrow in BrandRows:
		#	JsonResult = {}
		#	JsonResult['id'] = brandrow['brandname']
		#	JsonResult['label'] = brandrow['brandname']
		#	JsonResult['value'] = brandrow['brandname']
		#	results.append(JsonResult)
		#data = json.dumps(results,cls=DjangoJSONEncoder)
	return HttpResponse(json.dumps(result,cls=DjangoJSONEncoder),status = 500, content_type='application/json')
@ensure_csrf_cookie
def SearchGoodsbyForm(request):
	"""get goods data for grid searching, retusn idapp,itemcode,goods criteria = icontains"""
	Isidx = request.GET.get('sidx', '')
	Isord = request.GET.get('sord', '')
	
			
	searchText = request.GET.get('goods_desc')
	Ilimit = request.GET.get('rows', '')
	NAData = None;
	if(Isord is not None and str(Isord) != ''):
		NAData = goods.customs.searchGoodsByForm(searchText).order_by('-' + str(Isidx))
	else:
		NAData = goods.customs.searchGoodsByForm(searchText)
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
	i = 0;#idapp,itemcode,goods
	for row in dataRows.object_list:
		i+=1
		datarow = {"id" :str(row['idapp']) +'_fk_goods', "cell" :[row['idapp'],i,row['itemcode'],row['goods']]}
		rows.append(datarow)
	results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
	return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
def SearchSuplierbyForm(request):
	"""get suplier data for grid return suplier code,supliername, criteria = icontains"""
	searchText = request.GET.get('supliername')
	Ilimit = request.GET.get('rows', '')
	Isidx = request.GET.get('sidx', '')
	Isord = request.GET.get('sord', '')
	NAData = None;
	if(Isord is not None and str(Isord) != ''):
		NAData = NASuplier.customManager.getSuplierByForm(searchText).order_by('-' + str(Isidx))
	else:
		NAData = NASuplier.customManager.getSuplierByForm(searchText)
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
	i = 0;#idapp,itemcode,goods
	for row in dataRows.object_list:
		i+=1
		datarow = {"id" :row['supliercode'], "cell" :[i,row['supliercode'],row['supliername']]}
		rows.append(datarow)
	results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
	return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
def SearchEmployeebyform(request):
	"""get employee data for grid return idapp,nik, employee_name criteria = icontains"""
	searchText = request.GET.get('employee_name')
	Ilimit = request.GET.get('rows', '')
	Isidx = request.GET.get('sidx', '')
	Isord = request.GET.get('sord', '')
	if(Isord is not None and str(Isord) != ''):
		NAData = Employee.customManager.getEmloyeebyForm(searchText).order_by('-' + str(Isidx))
	else:
		NAData = Employee.customManager.getEmloyeebyForm(searchText)
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
	i = 0;#idapp,itemcode,goods
	for row in dataRows.object_list:
		datarow = {"id" :row['idapp'], "cell" :[row['idapp'],i+1,row['nik'],row['employee_name']]}
		rows.append(datarow)
	results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
	return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
class NA_Goods_Receive_Form(forms.Form):
	idapp  = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	
	fk_goods = forms.CharField(widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:100px;display:inline-block;margin-right:5px;','tabindex':1,
                                   'placeholder': 'goods item code','data-value':'goods item code','tittle':'Please enter item code'}),required=True)
	goods_desc = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','readonly':True,
																						 'placeholder': 'goods item code','data-value':'goods item code','tittle':'goods Desc is required'}))
	 
	fk_suplier = forms.CharField(max_length=30,widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:100px;display:inline-block;margin-right:5px;','tabindex':2,
                                   'placeholder': 'suplier code','data-value':'suplier code','tittle':'Please enter suplier code'}),required=True)
	supliername = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','readonly':True,
																						 'placeholder': 'suplier name','data-value':'suplier name','tittle':'suplier name is required'}))
	datereceived = forms.DateField(required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:100px;display:inline-block;margin-right:5px;','tabindex':3,
                                   'placeholder': 'dd/mm/yyyy','data-value':'dd/mm/yyyy','tittle':'Please enter Date Received','patern':'((((0[13578]|1[02])\/(0[1-9]|1[0-9]|2[0-9]|3[01]))|((0[469]|11)\/(0[1-9]|1[0-9]|2[0-9]|3[0]))|((02)(\/(0[1-9]|1[0-9]|2[0-8]))))\/(19([6-9][0-9])|20([0-9][0-9])))|((02)\/(29)\/(19(6[048]|7[26]|8[048]|9[26])|20(0[048]|1[26]|2[048])))'}))
	totalpurchase = forms.IntegerField(max_value=1000,required=True,widget=forms.NumberInput(attrs={'class': 'NA-Form-Control','maxlength':4, 'min':1, 'max':9000,'tabindex':4,'style':'width:82px;;display:inline-block;margin-right:5px;','placeholder': 'Total Purchased','data-value':'Total Purchased','tittle':'Total purchased is required','patern':'[1-9]\d{1,9}','step':'any'}))
	totalreceived = forms.IntegerField(max_value=1000,required=True,widget=forms.NumberInput(attrs={'class': 'NA-Form-Control','maxlength':4, 'min':1, 'max':9000,'tabindex':5,'style':'width:82px;;display:inline-block;margin-right:5px;','placeholder': 'Total Purchased','data-value':'Total Purchased','tittle':'Total purchased is required','patern':'[1-9]\d{1,9}','step':'any'}))
	fk_p_r_by = forms.CharField(max_length=30,widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:100px;display:inline-block;margin-right:5px;','tabindex':6,
                                   'placeholder': 'P R By','data-value':'P R By','tittle':'Employee code(NIK) who PRs'}),required=True)
	employee_pr = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','readonly':True,
																						 'placeholder': 'Employee who PRs','data-value':'Employee who PRs','tittle':'Employee who PRs is required'}))
	fk_receivedby = forms.CharField(max_length=30,widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:100px;display:inline-block;margin-right:5px;','tabindex':7,
                                   'placeholder': 'Who Receives','data-value':'Who Receives','tittle':'Employee code(NIK) who Receives'}),required=True)
	employee_received = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','readonly':True,
																						 'placeholder': 'Employee who Receives','data-value':'Employee who Receives','tittle':'Employee who Receives is required'}))
	descriptions = forms.CharField(max_length=250,widget=forms.Textarea(attrs={'cols':'100','rows':'2','tabindex':8,'style':'max-width: 520px;width: 444px;height: 45px;','class':'NA-Form-Control','placeholder':'descriptions about goods received (remark)','data-value':'descriptions about goods received (remark)'}),required=False) # models.CharField(db_column='Descriptions', max_length=150, blank=True, null=True)  # Field name made lowercase.
	idapp_fk_goods = forms.IntegerField(widget=forms.HiddenInput())
	idapp_fk_p_r_by = forms.IntegerField(widget=forms.HiddenInput())
	idapp_fk_receivedby = forms.IntegerField(widget=forms.HiddenInput())
	status = forms.CharField(widget=forms.HiddenInput())
		#initializeForm = forms.CharField(widget=forms.HiddenInput(attrs={'value':{'depreciationmethod':'SL','economiclife':5.00,'placement':'Gudang IT','inactive':False}}),required=False)
	initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)
	hasRefData = forms.BooleanField(widget=forms.HiddenInput(),required=False)
	
	#class Meta:
	#	model = NAGoodsReceive
	#	exclude = ('createdby','createddate','modifiedby','modifieddate')
	def clean(self):#fk_goods, datereceived, fk_suplier, totalpurchase, totalreceived,  fk_receivedby fk_p_r_by, idapp_fk_goods, idapp_fk_p_r_by, idapp_fk_receivedby,descriptions
		cleaned_data = super(NA_Goods_Receive_Form,self).clean()
		fk_goods = self.cleaned_data.get('fk_goods')
		datereceived = self.cleaned_data.get('datereceived')
		fk_suplier = self.cleaned_data.get('fk_suplier')
		totalpurchase = self.cleaned_data.get('totalpurchase')
		totalreceived = self.cleaned_data.get('totalreceived')
		fk_receivedby = self.cleaned_data.get('fk_receivedby')
		fk_p_r_by = self.cleaned_data.get('fk_p_r_by')
		idapp_fk_goods = self.cleaned_data.get('idapp_fk_goods')
		idapp_fk_p_r_by = self.cleaned_data.get('idapp_fk_p_r_by')
		idapp_fk_receivedby = self.cleaned_data.get('idapp_fk_receivedby')
		descriptions = self.cleaned_data.get('descriptions')
		hasRefData = self.cleaned_data.get('hasRefData')
