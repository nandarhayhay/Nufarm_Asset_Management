from django.shortcuts import render
from NA_Models.models import NAAccFa, goods
from django import forms
from django.http import HttpResponse, JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from NA_DataLayer.common import CriteriaSearch
from NA_DataLayer.common import ResolveCriteria
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import datetime
from dateutil import relativedelta

def NA_AccGetData(request):
    IcolumnName = request.GET.get('columnName')
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
        accData = NAAccFa.objects.PopulateQuery(IcolumnName,IvalueKey,criteria,dataType).order_by('-' + str(Isidx))
    else:
        accData = NAAccFa.objects.PopulateQuery(IcolumnName,IvalueKey,criteria,dataType)			

    totalRecord = accData.count()
    paginator = Paginator(accData, int(Ilimit)) 
    try:
        page = request.GET.get('page', '1')
    except ValueError:
        page = 1
    try:
        data = paginator.page(page)
    except (EmptyPage, InvalidPage):
        data = paginator.page(paginator.num_pages)

    rows = []
    for row in data.object_list:
        datarow = {"id" :row['idapp'], "cell" :[row['idapp'],row['fk_goods'],row['year'],row['startdate'],row['depr_expense'],\
			row['depr_accumulation'],row['bookvalue'],row['createddate'],row['createdby']]}
        rows.append(datarow)
    results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
    return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')


class NA_Acc_Form(forms.Form):
	fk_goods = forms.CharField(required=True,widget=forms.TextInput(attrs={
		'class':'NA-Form-Control'
		}))
	year = forms.CharField(required=False,widget=forms.TextInput(attrs={
		'class':'NA-Form-Control','disabled':'true'
		}))
	startdate = forms.CharField(required=True,widget=forms.TextInput(attrs={
		'class':'NA-Form-Control','disabled':'true'
		}))
	depr_expense = forms.DecimalField(required=True,widget=forms.TextInput(attrs={
		'class':'NA-Form-Control','disabled':'true'
		}))
	depr_accumulation = forms.DecimalField(required=True,widget=forms.TextInput(attrs={
		'class':'NA-Form-Control','disabled':'true'
		}))
	book_value = forms.DecimalField(required=True,widget=forms.TextInput(attrs={
		'class':'NA-Form-Control','disabled':'true'
		}))
	initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)

def NA_Acc_FA(request):
    return render(request,'app/MasterData/NA_F_Acc_FA.html')

def getData(request, forms):
	clData = forms.cleaned_data
	data = {
		'fk_goods': clData['fk_goods'],
		'year': clData['year'],
		'startdate': clData['startdate'],
		'depr_expense': clData['depr_expense'],
		'depr_accumulation': clData['depr_accumulation'],
		'bookvalue': clData['book_value']
		}
	return data

def EntryAcc(request):
	if request.method == 'POST':
		form = NA_Acc_Form(request.POST)
		if form.is_valid():
			data = getData(request,form)
			if request.POST['mode'] == 'Add':
				data['createddate'] = datetime.datetime.now()
				data['createdby'] = str(request.user.username)
				NAAccFa.objects.create_acc_FA(**data)
			elif request.POST['mode'] == 'Edit':
				pass

			return HttpResponse('success')
		else:
			return HttpResponse('gagal', status=403)
	elif request.method == 'GET':
		form = NA_Acc_Form()
		return render(request,'app/MasterData/Entry_AccFA.html',{'form':form})
def searchGoods(request):
	if request.is_ajax() and request.method == 'GET':
		term = request.GET['term']
		result = goods.objects.filter(goodsname__contains=term).values('idapp','goodsname')
		result_search = []
		for i in result:
			data = {}
			data['value'] = str(i['idapp'])
			data['label'] = i['goodsname']
			result_search.append(data)
		return HttpResponse(json.dumps(result_search,cls=DjangoJSONEncoder))

def getGoods_data(request):
	if request.is_ajax() and request.method == 'POST':
		idapp = request.POST['idapp']
		goods_data = goods.objects.filter(idapp=idapp).values('economiclife','createddate','depreciationmethod','priceperunit')[0]
		economiclife = goods_data['economiclife']
		priceperunit = goods_data['priceperunit']
		createddate = goods_data['createddate'].date()
		now = datetime.datetime.now().date()
		if goods_data['depreciationmethod'] == 'SL' or goods_data['depreciationmethod'] == 'DDB':
			rd = relativedelta.relativedelta(now,createddate)
			get_year = rd.years
			depr_expense = int(priceperunit)/(int(economiclife)*12)
			get_month = rd.months
			total_month = (get_year*12) + get_month
			if goods_data['depreciationmethod'] == 'SL':
				depr_accumulation = depr_expense*total_month
			elif goods_data['depreciationmethod'] == 'DDB':
				depr_accumulation = 2*(depr_expense*total_month)
			book_value = int(priceperunit)-int(depr_accumulation)
		elif goods_data['depreciationmethod'] == 'STYD':
			get_ecLife = datetime.date(createddate.year+int(economiclife),createddate.month,createddate.day)
			rd = relativedelta.relativedelta(get_ecLife,createddate)
			get_year = rd.years
			dig_year = int(economiclife) #assign it to variabel for looping , without minus value of economiclife :D
			total_year = 0 #total arr_year :D
			arr_year = [] # e.g [4,3,2,1] :D
			depr_accumulation = 0
			get_depr_acc = 0
			book_value = 0
			for i in range(dig_year):
				arr_year.append(dig_year)
				total_year +=dig_year
				dig_year -= 1 #minus dig_year until 0, and break .. for getting result [4,3,2,1] :D
			for i in arr_year:
				get_depr_acc +=i
				if i <= int(economiclife):
					break
			if get_depr_acc > 0:
				depr_accumulation = (get_depr_acc/total_year)*int(priceperunit)
				book_value = int(priceperunit)-int(depr_accumulation)
			depr_expense = (get_year/total_year)*int(priceperunit)
		data = [{
				#'total_month':total_month,
				'startdate':createddate,
				'year':goods_data['economiclife'],
				'depr_expense':'%0.2f' % depr_expense,
				'depr_accumulation':'%0.2f' % depr_accumulation,
				'book_value':'%0.2f' % book_value
				}]
		return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder),content_type='application/json')

	#4/10 * 1.000.000
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#