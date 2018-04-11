from NA_Models.models import NAGoodsLost, goods, Employee
from django.http import HttpResponse
import json
from NA_DataLayer.common import ResolveCriteria, commonFunct, StatusForm
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from django import forms
from datetime import datetime
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def NA_Goods_Lost(request):
    return render(request,'app/MasterData/NA_F_GoodsLost.html')

def NA_GoodsLost_GetData(request):
    IcolumnName = request.GET.get('columnName')
    IvalueKey =  request.GET.get('valueKey')
    IdataType =  request.GET.get('dataType')
    Icriteria =  request.GET.get('criteria')
    Ilimit = request.GET.get('rows', '')
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    Ipage = request.GET.get('page')
    getColumn = commonFunct.retriveColumn(
		table=[NAGoodsLost,goods],resolve=IcolumnName,
		initial_name=['gls','g','empl1','empl2','empl3'],
		custom_fields=[['used_by'],['lost_by'],['resp_person']])
    criteria = ResolveCriteria.getCriteriaSearch(str(Icriteria))
    dataType = ResolveCriteria.getDataType(str(IdataType))
    accData = NAGoodsLost.objects.PopulateQuery(IcolumnName,IvalueKey,criteria,dataType,Isidx,Isord)
    paginator = Paginator(accData,Ilimit)
    try:
        dataRows = paginator.page(Ipage)
    except EmptyPage:
        dataRows = paginator.page(paginator.num_pages)
    totalRecord = len(accData)
    rows = []
    i = 0
    for row in dataRows.object_list:
        i +=1
        datarow = {"id" :row['idapp'], "cell" :[row['idapp'],i,row['goods'],row['itemcode'],row['serialnumber'],row['fk_fromgoods'],row['used_by'],\
            row['lost_by'],row['resp_person'],row['descriptions'],row['createddate'],row['createdby']]}
        rows.append(datarow)
    results = {"page": Ipage,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
    return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')

def ShowCustomFilter(request):
	if request.is_ajax():
		cols = []
		cols.append({'name':'goodsname','value':'goodsname','selected':'True','dataType':'varchar','text':'Goods Name'})
		cols.append({'name':'brandname','value':'brandname','selected':'','dataType':'varchar','text':'Brand Name'})
		cols.append({'name':'itemcode','value':'itemcode','selected':'','dataType':'varchar','text':'Item code'})
		cols.append({'name':'serialnumber','value':'serialnumber','selected':'','dataType':'varchar','text':'Serial Number'})
		cols.append({'name':'used_by','value':'used_by','selected':'','dataType':'varchar','text':'Used by'})
		cols.append({'name':'lost_by','value':'lost_by','selected':'','dataType':'varchar','text':'Lost by'})
		cols.append({'name':'resp_person','value':'resp_person','selected':'','dataType':'varchar','text':'Responsible Person'})
		cols.append({'name':'descriptions','value':'descriptions','selected':'','dataType':'varchar','text':'Descriptions'})
		return render(request, 'app/UserControl/customFilter.html', {'cols': cols})

class NA_GoodsLost_Form(forms.Form):
    fk_goods = forms.IntegerField(required=True,widget=forms.HiddenInput())
    fk_fromgoods = forms.CharField(required=False,widget=forms.HiddenInput())
    goods = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control cust-horizontal','disabled':'disabled','style':'width:155px','placeholder':'goods'}))
    itemcode = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control cust-horizontal','placeholder':'Item code','style':'width:130px'}))
    typeApp = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control cust-horizontal','disabled':'disabled','placeholder':'Type of goods','style':'width:130px'}))
    serialNumber = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control cust-horizontal','disabled':'disabled','placeholder':'Serial Number','style':'width:195px'}))
    nik_used = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control cust-horizontal','disabled':'disabled','placeholder':'Nik','style':'width:130px'}))
    empl_used = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control cust-horizontal','placeholder':'Employee who wear','style':'width:195px','disabled':'disabled'}))
    fk_lostby = forms.IntegerField(required=False,widget=forms.HiddenInput())
    nik_lostby = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control cust-horizontal','disabled':'disabled','placeholder':'Nik','style':'width:130px','disabled':'disabled'}))
    empl_lostby = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control cust-horizontal','placeholder':'Employee who lost goods','style':'width:155px','disabled':'disabled'}))
    nik_resp = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control cust-horizontal','placeholder':'Nik','style':'width:130px','disabled':'disabled'}))
    empl_resp = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control cust-horizontal','placeholder':'Responsible person','style':'width:195px','disabled':'disabled'}))
    datelost = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control cust-horizontal','placeholder':'Date Lost','style':'width:130px'}))
    status_goods = forms.ChoiceField(required=False,widget=forms.Select(attrs={
                    'class':'NA-Form-Control', 'style':'width:130px;display:inline-block;'}),choices=(('L','Lost'),('F','Find')))
    reason = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class':'NA-Form-Control','placeholder':'reason .. .', 'style':'width:195px;height:50px;max-width:195px;max-height:125px;'}))
    descriptions = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class':'NA-Form-Control','placeholder':'descriptions .. .', 'style':'width:243px;height:50px;max-width:243px;max-height:125px;'}))
    fk_goods_outwards = forms.IntegerField(required=False,widget=forms.HiddenInput())
    fk_goods_lending = forms.IntegerField(required=False,widget=forms.HiddenInput())
    fk_maintenance = forms.IntegerField(required=False,widget=forms.HiddenInput())
    initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)

def getFormData(request, forms, **kwargs):
    clData = forms.cleaned_data
    data = {
        'fk_goods': clData['fk_goods'],'goods': clData['goods'],'typeApp':clData['typeApp'],
        'serialNumber':clData['serialNumber'],'fk_fromgoods':clData['fk_fromgoods'],'fk_goods_outwards': clData['fk_goods_outwards'],
        'fk_goods_lending': clData['fk_goods_lending'],'fk_maintenance': clData['fk_maintenance'],'fk_lostby':clData['fk_lostby'],
        'datelost':clData['datelost'],'reason':clData['reason'],'descriptions': clData['descriptions']
        }
    if 'status_form' in kwargs:
        if kwargs['status_form'] == 'Edit' or kwargs['status_form'] == 'Open':
            data['status_goods'] = request.POST['status_goods']
    return data

def EntryGoods_Lost(request):
    if request.method == 'POST':
        form = NA_GoodsLost_Form(request.POST)
        if form.is_valid():
            statusForm = request.POST['statusForm']
            if statusForm == 'Add':
                data = getFormData(request, form)
                createddate = datetime.now()
                createdby = request.user.username
                data['createddate'] = createddate
                data['createdby'] = createdby
                result = NAGoodsLost.objects.SaveData(StatusForm.Input, **data)
                #statusResp = 200
                #if result[0] != 'success':
                #    statusResp = 500
                #return HttpResponse(json.dumps(result), status=statusResp, content_type='application/json')
            elif statusForm == 'Edit':
                data = getFormData(request, form, status_form='Edit')
                idapp = request.POST['idapp']
                data['idapp'] = idapp
                data['modifieddate'] = datetime.now()
                data['modifiedby'] = request.user.username
                result = NAGoodsLost.objects.SaveData(StatusForm.Edit, **data)
            statusResp = 200
            if result[0] != 'success':
                statusResp = 500
            return HttpResponse(json.dumps(result), status=statusResp, content_type='application/json')
        elif not form.is_valid():
            return HttpResponse('form not valid',status=403)
    elif request.method == 'GET':
        idapp = request.GET['idapp']
        statusForm = request.GET['statusForm']
        if statusForm == 'Edit' or statusForm == 'Open':
            result = NAGoodsLost.objects.retriveData(idapp)
            if result[0] == 'success':
                form = NA_GoodsLost_Form(initial=result[1])
                #form.fields['status_goods'] = forms.ChoiceField(required=False,widget=forms.Select(attrs={
                #    'class':'NA-Form-Control', 'style':'width:130px;'}),choices=(('L','Lost'),('F','Find')))
            elif result[0] == 'Lost':
                return HttpResponse('Lost',status=404)
        else:
            form = NA_GoodsLost_Form()
        form.statusForm = statusForm
        return render(request, 'app/MasterData/NA_Entry_GoodsLost.html', {'form':form})

def SearchGoodsbyForm(request):
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    goodsFilter = request.GET.get('goods_filter')
    tabs_section = request.GET.get('tab_section')
    Ilimit = request.GET.get('rows', '')
    NAData = NAGoodsLost.objects.searchGoods_byForm({'goods_filter':goodsFilter,'tab_section':tabs_section})
    if NAData[1] == []:
        results = {"page": "1","total": 0 ,"records": 0,"rows": [] }
    else:
        totalRecord = len(NAData[1])
        paginator = Paginator(NAData[1], int(Ilimit)) 
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
        if NAData[0] == 'g_maintenance':
            for row in dataRows.object_list:
                i+=1
                datarow = {"id" :str(row['idapp']) +'_fk_goods', "cell" :[row['idapp'],row['fk_goods'],i,row['itemcode'],row['goods'],\
                    row['serialnumber'],row['tbl_name']]}
                rows.append(datarow)
        else:
            for row in dataRows.object_list:
                i+=1
                datarow = {"id" :str(row['idapp']) +'_fk_goods', "cell" :[row['idapp'],row['fk_goods'],i,row['itemcode'],row['goods'],\
                    row['serialnumber'],row['tbl_name'],row['fk_employee'],row['fk_resp'],row['nik_employee'],row['nik_resp']]}
                rows.append(datarow)
        results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
    return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')

def SearchEmployeebyform(request):
	searchText = request.GET.get('employee_filter')
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
	i = 0;
	for row in dataRows.object_list:
		i+=1
		datarow = {"id" :row['idapp'], "cell" :[row['idapp'],i,row['nik'],row['employee_name']]}
		rows.append(datarow)
	results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
	return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')