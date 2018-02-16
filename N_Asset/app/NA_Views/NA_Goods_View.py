from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.utils.dateformat import DateFormat
from NA_Models.models import goods, LogEvent
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
import decimal
def NA_Goods(request):
	assert isinstance(request,HttpRequest)
	#buat nama-name column, key sama 
	populate_combo = []
	populate_combo.append({'label':'ItemCode','columnName':'itemcode','dataType':'varchar'})
	populate_combo.append({'label':'BrandName','columnName':'brandname','dataType':'varchar'})
	populate_combo.append({'label':'PricePerUnit','columnName':'priceperUnit','dataType':'decimal'})
	populate_combo.append({'label':'Depreciation_Method','columnName':'depreciationmethod','dataType':'char'})
	populate_combo.append({'label':'unit','columnName':'economiclife','dataType':'decimal'})
	populate_combo.append({'label':'Placement','columnName':'placement','dataType':'varchar'})
	return render(request,'app/MasterData/NA_F_Goods.html',{'populateColumn':populate_combo})
	
#@decorators.ajax_required
def NA_Goods_Search(request):	
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
		NAData = goods.objects.PopulateQuery(IcolumnName,IvalueKey,criteria,dataType).order_by('-' + str(Isidx))
	else:
		NAData = goods.objects.PopulateQuery(IcolumnName,IvalueKey,criteria,dataType)			
#		from django.db.models import F
#cityList = City.objects.using(settings.DATABASE_CONF).filter(status=1).values(
#    'city_name_en', 'city_id')
## use F expression to annotate with an alias
#cityList = cityList.annotate(cityname=F('city_name_en'))
	
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
	for row in dataRows.object_list:
		datarow = {"id" :row['idapp'], "cell" :[row['idapp'],row['itemcode'],row['goodsname'],row['brandname'],row['unit'],row['priceperunit'], \
			row['placement'],row['typeofdepreciation'],row['economiclife'],row['inactive'],datetime.date(row['createddate']),row['createdby']]}
		#datarow = {"id" :row.idapp, "cell" :[row.idapp,row.itemcode,row.goodsname,row.brandname,row.unit,row.priceperunit, \
		#	row.placement,row.depreciationmethod,row.economiclife,row.createddate,row.createdby]}
		rows.append(datarow)
	results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
	return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
def Search_Good(request):
	if(request.is_ajax()):
		IvalueKey =  request.GET.get('term')
		BrandRows = goods.objects.SearchBrand(IvalueKey)
		results = []
		for brandrow in BrandRows:
			JsonResult = {}
			JsonResult['id'] = brandrow['brandname']
			JsonResult['label'] = brandrow['brandname']
			JsonResult['value'] = brandrow['brandname']
			results.append(JsonResult)
		data = json.dumps(results,cls=DjangoJSONEncoder)
		return HttpResponse(data, content_type='application/json')
	else:
		return HttpResponse(content='',content_type='application/json')
def Search_Brand(request):
	if(request.is_ajax()):
		IvalueKey =  request.GET.get('term')
		BrandRows = goods.objects.SearchBrand(IvalueKey)
		results = []
		for brandrow in BrandRows:
			JsonResult = {}
			JsonResult['id'] = brandrow['brandname']
			JsonResult['label'] = brandrow['brandname']
			JsonResult['value'] = brandrow['brandname']
			results.append(JsonResult)
		data = json.dumps(results,cls=DjangoJSONEncoder)
		return HttpResponse(data, content_type='application/json')
	else:
		return HttpResponse(content='',content_type='application/json')
def getCurrentDataModel(request,form):	
	return {'itemcode':form.cleaned_data['itemcode'],'goodsname':form.cleaned_data['goodsname'],'brandname':form.cleaned_data['brandname'],
		 'typeapp':form.cleaned_data['typeapp'],'unit':form.cleaned_data['unit'],'priceperunit':decimal.Decimal(form.cleaned_data['priceperunit']),
		 'depreciationmethod':form.cleaned_data['depreciationmethod'],'economiclife':decimal.Decimal(form.cleaned_data['economiclife'])
		 ,'placement':form.cleaned_data['placement'],'descriptions':request.POST.get('descriptions'),'inactive':True if request.POST.get('inactive') == 'true' else False,'createddate':str(datetime.now().date()),'createdby':request.user.username if request.user.username is not None and request.user != '' else 'Admin' }
@ensure_csrf_cookie
def ShowEntry(request):
	authentication_classes = []
	status = 'Add'
	itemcode=''
	initializationForm={}
	statuscode = 200
	if(request.POST):
		status = request.POST.get('status')
	else:
		status = 'Add' if request.GET.get('status') == None else request.GET.get('status')
		itemcode = request.GET.get('itemcode')	
		initializationForm = {'depreciationmethod':'SL','economiclife':5.00,'placement':'Gudang IT','inactive':False,'hasRefData':'false'}
	#form = NA_Goods_Form(initial=initializationForm)
	#form.fields['status'].widget.attrs = {'value':status};	
	#form.fields['initializeForm'].widget.attrs = json.dumps({'value':initializationForm}) if status == "Add" or status == "Edit" else None
	if request.is_ajax():		
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
	#					IcolumnName = request.GET.get('columnName');
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
				#form.fields['initializeForm'].widget.attrs = {'value':json.dumps(initializationForm)}
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
					data['modifieddate'] = datetime.now()
					data['modifiedby'] = request.user.username
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
def setInActive(request):
	result = '';
	try:
		idapp = request.GET.get('idapp');
		inactive = request.GET.get('inactive');
		goods.objects.setInActive(idapp,strtobool(str(inactive)))
		return HttpResponse(json.dumps({'message':'success'}),status = 200, content_type='application/json') 
	except Exception as e:					
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
def deleteItem(request):
	result='';
	try:
		itemcode = request.GET.get('itemCode')
		log_goods = goods.objects.filter(itemcode=itemcode).values('itemcode','goodsname','brandname','typeapp','priceperunit',\
			'depreciationmethod','unit','economiclife','placement','descriptions','inactive','createdby','createddate', 'modifieddate', 'modifiedby')[0]
		hasref = goods.objects.hasreferenced(itemcode)
		if hasref:
			return HttpResponse(json.dumps({'message':'can not delete data \nData has referenced child data'}),status = 500, content_type='application/json')
		LogEvent.objects.create(nameapp='Deleted Goods',typeapp='P', descriptionsapp={
                    'deleted':[
                        log_goods['itemcode'],
                        log_goods['goodsname'],
						log_goods['brandname'],
                        log_goods['typeapp'],
                        str(log_goods['priceperunit']),
                        log_goods['depreciationmethod'],
                        log_goods['unit'],
                        str(log_goods['economiclife']),
                        log_goods['placement'],
                        log_goods['descriptions'],
                        log_goods['inactive'],
                        log_goods['createddate'].strftime('%d %B %Y %H:%M:%S'),
                        log_goods['createdby'],
                        log_goods['modifieddate'],
                        log_goods['modifiedby']
                        ]
                    }, createdby=str(request.user.username))
		goods.objects.Delete(itemcode)
		return HttpResponse(json.dumps({'message':'success'}),status = 200, content_type='application/json') 
	except Exception as e:					
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
def ShowCustomFilter(request):
	if request.is_ajax():
		cols = []
		cols.append({'name':'itemcode','value':'itemcode','selected':'','dataType':'varchar','text':'item code'})
		cols.append({'name':'goodsname','value':'goodsname','selected':'True','dataType':'varchar','text':'goods name'})
		cols.append({'name':'brandname','value':'brandname','selected':'','dataType':'varchar','text':'brand name'})
		cols.append({'name':'typeapp','value':'typeapp','selected':'','dataType':'varchar','text':'type of brand'})
		cols.append({'name':'unit','value':'unit','selected':'','dataType':'varchar','text':'unit of goods'})
		cols.append({'name':'priceperunit','value':'priceperunit','selected':'','dataType':'decimal','text':'price per unit'})
		cols.append({'name':'depreciationmethod','value':'depreciationmethod','selected':'','dataType':'decimal','text':'Depreciation Method'})
		cols.append({'name':'economiclife','value':'economiclife','selected':'','dataType':'decimal','text':'Ecopnomic Life'})
		cols.append({'name':'placement','value':'placement','selected':'','dataType':'varchar','text':'placement'})
		cols.append({'name':'descriptions','value':'descriptions','selected':'','dataType':'varchar','text':'Descriptions'})
		cols.append({'name':'inactive','value':'inactive','selected':'','dataType':'boolean','text':'InActive'})
		return render(request, 'app/UserControl/customFilter.html', {'cols': cols})	

class NA_Goods_Form(forms.Form):
		#idapp = models.IntegerField(db_column='IDApp',primary_key=True)  # Field name made lowercase.
		"""
		There are many other types of form fields, which you will largely recognise from their similarity to the equivalent model field classes:
	    
		BooleanField, CharField, ChoiceField, TypedChoiceField, DateField, DateTimeField, DecimalField, DurationField, EmailField, FileField, FilePathField, 
		FloatField, ImageField, IntegerField, GenericIPAddressField, MultipleChoiceField, TypedMultipleChoiceField, NullBooleanField, RegexField, SlugField, 
		TimeField, URLField, UUIDField, ComboField, MultiValueField, SplitDateTimeField, ModelMultipleChoiceField, ModelChoiceField​​​​.
		for
		The arguments that are common to most fields are listed below (these have sensible default values):
		required: If True, the field may not be left blank or given a None value. Fields are required by default, so you would set required=False to allow blank values in the form.
		label: The label to use when rendering the field in HTML. If label is not specified then Django would create one from the field name by capitalising the first letter and replacing underscores with spaces (e.g. Renewal date).
		label_suffix: By default a colon is displayed after the label (e.g. Renewal date:). This argument allows you to specify as different suffix containing other character(s).
		initial: The initial value for the field when the form is displayed.
		widget: The display widget to use.
		help_text (as seen in the example above): Additional text that can be displayed in forms to explain how to use the field.
		error_messages: A list of error messages for the field. You can override these with your own messages if needed.
		validators: A list of functions that will be called on the field when it is validated.
		localize: Enables the localisation of form data input (see link for more information).
		disabled: The field is displayed but its value cannot be edited if this is True. The default is False.
		"""
		idapp  = forms.IntegerField(widget=forms.HiddenInput(),required=False)
		itemcode = forms.CharField(max_length=30,required=True, widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:100px',
                                   'placeholder': 'item code','data-value':'item code','tittle':'Please enter item code'})) 
		goodsname = forms.CharField(max_length=150,widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:150px;margin-left:3px;',
                                   'placeholder': 'enter goods name','data-value':'enter goods name','tittle':'Please enter goods name'}),required=True)  # models.CharField(db_column='GoodsName', max_length=100)  # Field name made lowercase.
		brandname = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:250px;margin-left:3px;','placeholder':'enter brand','data-value':'enter brand','tittle':'Please enter valid brand name'}),required=True) #models.CharField(db_column='BrandName', max_length=100, blank=True, null=True)  # Field name made lowercase.
		typeapp = forms.CharField(max_length=32,required=True,widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:100px','placeholder':'enter type','data-value':'enter type','tittle':'Please enter type'}))  
		priceperunit = forms.DecimalField(max_digits=30,decimal_places=2,widget=forms.TextInput(attrs={
									'class':'NA-Form-Control','style':'width:150px;','placeholder':'price','data-value':'price','patern':'^[0-9]+([\.,][0-9]+)?$','step':'any','tittle':'Please enter valid value'}),required=True)#  models.DecimalField(db_column='PricePerUnit', max_digits=20,decimal_places=4)  # Field name made lowercase.
		depreciationmethod = forms.ChoiceField(widget=forms.Select(attrs={
                                   'class': 'NA-Form-Control select','style':'width:256px;margin-left:auto;'}),choices=(('SL', 'Straight Line Method'),
																	  ('DDB','Double Declining Balance'),
																	  ('STYD','Sum of The Year Digit'),
																	  ('SH','Service Hours')))   # models.CharField(db_column='DepreciationMethod', max_length=2)  # Field name made lowercase.
		unit = forms.ChoiceField(widget=forms.Select(attrs={'class':'NA-Form-Control select','style':'width:100px',}),choices=(('Pcs','Pcs'),('Box','Dus/Karton')))# .CharField(db_column='Unit', max_length=30)  # Field name madelowercase.
		economiclife = forms.DecimalField(max_digits=4,decimal_places=2,required=True,widget=forms.NumberInput(attrs={'class':'NA-Form-Control','style':'width:92px;vertical-align:bottom','step':'0.5','tittle':'Please enter valid value'})) #ini manual saja pakai select combo models.DecimalField(db_column='EconomicLife', max_digits=10,decimal_places=2)  # Field name made lowercase.
		placement = forms.ChoiceField(widget=forms.Select(attrs={'class':'NA-Form-Control.select','style':'width:130px;'}),choices=(('Gudang IT','Gudang IT'),('Gudang 2','Gudang 2'),('Gudang 3','Gudang 3'))) # models.CharField(db_column='Placement', max_length=50, blank=True, null=True)  # Field name made lowercase.
		descriptions = forms.CharField(max_length=250,widget=forms.Textarea(attrs={'cols':'100','rows':'2','style':'max-width: 520px;height: 45px;','class':'NA-Form-Control','placeholder':'descriptions about goods','data-value':'descriptions about goods'}),required=False) # models.CharField(db_column='Descriptions', max_length=150, blank=True, null=True)  # Field name made lowercase.
		inactive = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
		status = forms.CharField(widget=forms.HiddenInput(),required=False)
		#initializeForm = forms.CharField(widget=forms.HiddenInput(attrs={'value':{'depreciationmethod':'SL','economiclife':5.00,'placement':'Gudang IT','inactive':False}}),required=False)
		initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)
		hasRefData = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
		class meta:
			model = goods
			exclude = ('createdby','createddate','modifiedby','modifieddate')
			#fields = ('itemcode','goodsname','brandname','typeapp','priceperunit','depreciationmethod','unit','economiclife','placement','descriptions','inactive')
			#exclude = {'status','initializeForm'
		def clean(self):
			cleaned_data = super(NA_Goods_Form,self).clean()
			itemcode = self.cleaned_data.get('itemcode')
			goodsname = self.cleaned_data.get('goodsname')
			brandname = self.cleaned_data.get('brandname')
			typeapp = self.cleaned_data.get('typeapp')
			priceperunit = self.cleaned_data.get('priceperunit')
			depreciationmethod = self.cleaned_data.get('depreciationmethod')
			unit = self.cleaned_data.get('unit')
			economiclife = self.cleaned_data.get('economiclife')
			placement = self.cleaned_data.get('placement')
			descriptions = self.cleaned_data.get('descriptions')