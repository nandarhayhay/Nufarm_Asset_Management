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
@ensure_csrf_cookie
def ShowEntry_Receive(request):
	authentication_classes = []
	status = 'Add'
	IDApp = 1
	initializationForm={}
	statuscode = 200
	if request.POST:
		status = request.POST.get('status')
	else:
		status = 'Add' if request.GET.get('status') == None else request.GET.get('status')
		IDApp = request.GET.get('IDApp')
		#set initilization
	if status == 'Add':		
		if request.POST:
			form = NA_Goods_Form(request.POST)
			statuscode = 200
			if form.is_valid():
				#save data
				#ALTER TABLE n_a_goods MODIFY IDApp INT AUTO_INCREMENT PRIMARY KEY
				form.clean()
					
				data = getCurrentDataModel(request,form);					
				result = goods.objects.SaveData(StatusForm.Input,**data)
				if result != 'success':
					statuscode = 500
				return HttpResponse(json.dumps({'message':result}),status = statuscode, content_type='application/json')
				#newItem = goods(**data)
					
				#newItem = 
#IcolumnName = request.GET.get('columnName');
#IvalueKey =  request.GET.get('valueKey')
#IdataType =  request.GET.get('dataType')
#Icriteria =  request.GET.get('criteria')
#Ilimit = request.GET.get('rows', '')
#Isidx = request.GET.get('sidx', '')
#Isord = request.GET.get('sord', '')
			else: 
				#form = NA_Goods_Form(initial=initializationForm)                  
				#return  render(request, 'app/MasterData/NA_Entry.html', {'form' : form}				
				return HttpResponse(json.dumps({'message':'invalid form data'}),status = 400, content_type='application/json')
		else:				
			form = NA_Goods_Form(initial=initializationForm)
			form.fields['status'].widget.attrs = {'value':status};	
			return render(request, 'app/MasterData/NA_Entry.html', {'form' : form})
	elif status == 'Edit' or status == "Open":		
		hasRefData = goods.objects.hasreferenced(itemcode)
		if request.POST:
			form = NA_Goods_Form(request.POST)
			if form.is_valid():
				form.clean()
				#save data	
				data = getCurrentDataModel(request,form);
				data.update(idapp=request.POST.get('idapp'))	
				
				if hasRefData:
					return HttpResponse(json.dumps({'message':'can not edit data \nData has referenced child data'}),status = statuscode, content_type='application/json')										
				result = goods.objects.SaveData(StatusForm.Edit,**data)
				if result != 'success':
					statuscode = 500
				return HttpResponse(json.dumps({'message':result}),status = statuscode, content_type='application/json')
				#check itemCode
				#if scorm.objects.filter(Header__id=qp.id).exists()				
				#return HttpResponse('success', 'text/plain')
		else:
				#get data from database
			Ndata = goods.objects.getData(itemcode)[0]				
			NAData = {'itemcode':Ndata.itemcode,'goodsname':Ndata.goodsname,'brandname':Ndata.brandname,'typeapp':Ndata.typeapp,'unit':Ndata.unit,
						'priceperunit':"{0:.2f}".format(Ndata.priceperunit),'depreciationmethod':Ndata.depreciationmethod,'economiclife':Ndata.economiclife
						,'placement':Ndata.placement,'descriptions':Ndata.descriptions,'inactive':Ndata.inactive,'status':status,'idapp':Ndata.idapp,'hasRefData':'true' if hasRefData==True else 'false'}
			NAData.update(initializeForm=json.dumps(NAData,cls=DjangoJSONEncoder)) 
			form = NA_Goods_Form(data=NAData)
			form.fields['status'].widget.attrs = {'value':status};	
			#form = NA_Goods_Form(data=None)				
			return render(request, 'app/MasterData/NA_Entry.html', {'form' : form})
	else:
		return render(request, 'app/MasterData/NA_Entry.html', {'form' : form})


class NA_Goods_Receive_Form(forms.Form):
	idapp  = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_goods = forms.IntegerField(widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:90px;display:inline-block;margin-right:5px;',
                                   'placeholder': 'goods item code','data-value':'goods item code','tittle':'Please enter item code'}),required=True)
	goods_desc = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:200px;display:inline-block;',
																						 'placeholder': 'goods item code','data-value':'goods item code','tittle':'goods Desc is required'}))
	 
	fk_suplier = forms.CharField(max_length=30,widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:90px;display:inline-block;margin-right:5px;',
                                   'placeholder': 'suplier code','data-value':'suplier code','tittle':'Please enter suplier code'}),required=True)
	supliername = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:150px;display:inline-block;',
																						 'placeholder': 'suplier name','data-value':'suplier name','tittle':'suplier name is required'}))
	daterecieved = forms.DateField(required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:100px;display:inline-block;margin-right:5px;',
                                   'placeholder': 'dd/mm/yyyy','data-value':'dd/mm/yyyy','tittle':'Please enter Date Received','patern':'((((0[13578]|1[02])\/(0[1-9]|1[0-9]|2[0-9]|3[01]))|((0[469]|11)\/(0[1-9]|1[0-9]|2[0-9]|3[0]))|((02)(\/(0[1-9]|1[0-9]|2[0-8]))))\/(19([6-9][0-9])|20([0-9][0-9])))|((02)\/(29)\/(19(6[048]|7[26]|8[048]|9[26])|20(0[048]|1[26]|2[048])))'}))
	total_purchase = forms.IntegerField(max_value=1000,required=True,widget=forms.NumberInput(attrs={'class': 'NA-Form-Control','style':'width:70px;display:inline-block;margin-right:5px;','placeholder': 'Total Purchased','data-value':'Total Purchased','tittle':'Total purchased is required','patern':'[1-9]\d{1,9}','step':'any'}))
	total_received = forms.IntegerField(max_value=1000,required=True,widget=forms.NumberInput(attrs={'class': 'NA-Form-Control','style':'width:70px;display:inline-block;margin-right:5px;','placeholder': 'Total Purchased','data-value':'Total Purchased','tittle':'Total purchased is required','patern':'[1-9]\d{1,9}','step':'any'}))
	pr_by = forms.CharField(max_length=30,widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:90px;display:inline-block;margin-right:5px;',
                                   'placeholder': 'P R By','data-value':'P R By','tittle':'Employee Code who PRs'}),required=True)
	employee_pr = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:150px;display:inline-block;',
																						 'placeholder': 'Employee who PRs','data-value':'Employee who PRs','tittle':'Employee who PRs is required'}))
	fk_receivedby = forms.CharField(max_length=30,widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:90px;display:inline-block;margin-right:5px;',
                                   'placeholder': 'Who Receives','data-value':'Who Receives','tittle':'Employee Code who Receives'}),required=True)
	employee_Received = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:150px;display:inline-block;',
																						 'placeholder': 'Employee who Receives','data-value':'Employee who Receives','tittle':'Employee who Receives is required'}))
	descriptions = forms.CharField(max_length=250,widget=forms.Textarea(attrs={'cols':'100','rows':'2','style':'max-width: 520px;height: 45px;','class':'NA-Form-Control','placeholder':'descriptions about goods received (remark)','data-value':'descriptions about goods received (remark)'}),required=False) # models.CharField(db_column='Descriptions', max_length=150, blank=True, null=True)  # Field name made lowercase.
	status = forms.CharField(widget=forms.HiddenInput(),required=False)
		#initializeForm = forms.CharField(widget=forms.HiddenInput(attrs={'value':{'depreciationmethod':'SL','economiclife':5.00,'placement':'Gudang IT','inactive':False}}),required=False)
	initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)
	hasRefData = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
	
	class Meta:
		model = NAGoodsReceive
		exclude = ('createdby','createddate','modifiedby','modifieddate')
	def clean(self):#fk_goods daterecieved fk_suplier totalpurchase totalrecieved  fk_receivedby fk_p_r_by
		cleaned_data = super(NA_Goods_Receive_Form,self).clean()
		fk_goods = self.cleaned_data.get('fk_goods')
		daterecieved = self.cleaned_data.get('daterecieved')
		fk_suplier = self.cleaned_data.get('fk_suplier')
		totalpurchase = self.cleaned_data.get('totalpurchase')
		totalrecieved = self.cleaned_data.get('totalrecieved')
		fk_receivedby = self.cleaned_data.get('fk_receivedby')
		fk_p_r_by = self.cleaned_data.get('fk_p_r_by')
		economiclife = self.cleaned_data.get('economiclife')
		placement = self.cleaned_data.get('placement')
		descriptions = self.cleaned_data.get('descriptions')