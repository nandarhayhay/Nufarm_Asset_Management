from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import json
from NA_DataLayer.common import ResolveCriteria, CriteriaSearch, commonFunct, StatusForm
from NA_Models.models import NAMaintenance,goods
from django import forms
from datetime import datetime

def NA_Maintenance(request):
    return render(request,'app/MasterData/NA_F_Maintenance.html')
def NA_MaintenanceGetData(request):
    IcolumnName = request.GET.get('columnName')
    IvalueKey =  request.GET.get('valueKey')
    IdataType =  request.GET.get('dataType')
    Icriteria =  request.GET.get('criteria')
    Ilimit = request.GET.get('rows', '')
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    Ipage = request.GET.get('page')
    criteria = ResolveCriteria.getCriteriaSearch(Icriteria)
    dataType = ResolveCriteria.getDataType(IdataType)
    getColumn = commonFunct.retriveColumn(table=[NAMaintenance,goods],resolve=IcolumnName,initial_name=['m','g'])
    maintenanceData = NAMaintenance.objects.PopulateQuery(getColumn,IvalueKey,criteria,dataType)
    totalRecords = len(maintenanceData)
    paginator = Paginator(maintenanceData,Ilimit)
    try:
        dataRows = paginator.page(Ipage)
    except EmptyPage:
        dataRows = paginator.page(paginator.num_pages)
    rows = []
    i = 0
    for row in dataRows.object_list:
        i+=1
        datarow = {"id" :row['idapp'], "cell" :[row['idapp'],i,row['goods'],row['itemcode'],row['serialnumber'],row['requestdate'],\
            row['startdate'],row['isstillguarantee'],row['expense'],row['maintenanceby'],row['personalname'],row['enddate'],row['issucced'],\
            row['descriptions'],row['createddate'],row['createdby']]}
        rows.append(datarow)
    results = {"page": Ipage,"total": paginator.num_pages ,"records": totalRecords,"rows": rows }
    return HttpResponse(json.dumps(results,cls=DjangoJSONEncoder),content_type='application/json')

def getFormData(request,form):
    clData = form.cleaned_data
    data = {'fk_goods':clData['fk_goods'],'typeApp':clData['typeApp'],'serialNum':clData['serialNum'],'itemcode':clData['itemcode'],'goods':clData['goods'],
            'requestdate':clData['requestdate'],'startdate':clData['startdate'],'isstillguarantee':clData['isstillguarantee'],'expense':clData['expense'],
            'maintenanceby':clData['maintenanceby'],'personalname':clData['personalname'],'issucced':clData['issucced'],'enddate':clData['enddate'],
            'descriptions':clData['descriptions']}
    return data
class NA_Maintenance_Form(forms.Form):
    fk_goods = forms.CharField(required=True,widget=forms.HiddenInput())
    itemcode = forms.CharField(required=True,label='Search goods',widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','placeholder':'Item code','style':'width:110px;'}))
    goods = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','disabled':'disabled','placeholder':'Goods'}))
    typeApp = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','disabled':'disabled','placeholder':'type of goods','style':'width:110px;'}))
    serialNum = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','disabled':'disabled','placeholder':'serial number','style':'width:180px;'}))
    minus = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','disabled':'disabled','placeholder':'minus','style':'width:227px;'}))
    requestdate = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','placeholder':'Request Date','style':'width:110px;'}))
    startdate = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','placeholder':'Start Date','style':'width:110px;'}))
    isstillguarantee = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={
        'style':'margin-left:15px;position:absolute','disabled':'disabled'}))
    expense = forms.DecimalField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','placeholder':'Expense','style':'width:180px;'}))
    maintenanceby = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','placeholder':'Maintenance By','style':'width:227px;'}))
    personalname = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','placeholder':'Personal Name','style':'width:180px;'}))
    issucced = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={
        'style':'margin-left:15px;position:absolute'}))
    enddate = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','placeholder':'End Date','style':'width:110px;'}))
    descriptions = forms.CharField(required=True,widget=forms.Textarea(attrs={
        'class':'NA-Form-Control','placeholder':'Descriptions','style':'width:415px;height:45px;max-width:415px'}))
    initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)

def EntryMaintenance(request):
    getUser = str(request.user.username)
    if request.method == 'POST':
        form = NA_Maintenance_Form(request.POST)
        if form.is_valid():
            data = getFormData(request,form)
            statusForm = request.POST['statusForm']
            if statusForm == 'Add':
                data['createddate'] = datetime.now()
                data['createdby'] = getUser
                result = NAMaintenance.objects.SaveData(StatusForm.Input,**data)
                statusResp = 200
                if result[0] != 'success' and result[0] != 'HasExist':
                    message = 'Fail'
                    statusResp = 500
                elif result[0] == 'HasExist':
                    statusResp = 403
                    message = 'This data has Exist'
                else:
                    message = result[1]
                return HttpResponse(json.dumps(message),status=statusResp,content_type='application/json')
            elif statusForm == 'Edit':
                idapp = request.POST['idapp']
                data['idapp'] = idapp
                #data['issucced'] = 1 if data['issucced'] == 'true' else 0
                data['modifieddate'] = datetime.now()
                data['modifiedby'] = getUser
                result = NAMaintenance.objects.SaveData(StatusForm.Edit,**data)
                statusResp = 200
                if result[0] != 'success':
                    message = 'Fail'
                    statusResp = 500
                else:
                    message = result[1]
                return HttpResponse(json.dumps(message, cls=DjangoJSONEncoder),status=statusResp,content_type='application/json')
    elif request.method == 'GET':
        statusForm = request.GET['statusForm']
        if statusForm == 'Edit' or statusForm == 'Open':
            idapp = request.GET['idapp']
            data = NAMaintenance.objects.retriveData(idapp) #tuple data
            statusResp = 200
            if data[0] == 'Lost':
                statusResp = 500
                return HttpResponse('Lost',status=statusResp)
            if statusResp == 200:
                data[1][0]['issucced'] = True if data[1][0]['issucced'] == 1 else False
                data[1][0]['requestdate'] = data[1][0]['requestdate'].strftime('%d/%m/%Y')
                data[1][0]['startdate'] = data[1][0]['startdate'].strftime('%d/%m/%Y')
                data[1][0]['enddate'] = data[1][0]['enddate'].strftime('%d/%m/%Y')
                form = NA_Maintenance_Form(initial=data[1][0])
                return render(request,'app/MasterData/NA_Entry_Maintenance.html',{'form':form})
        else:
            form = NA_Maintenance_Form()
        return render(request,'app/MasterData/NA_Entry_Maintenance.html',{'form':form})

def Delete_M_data(request):
    if request.user.is_authenticated() and request.method == 'POST':
        idapp = request.POST['idapp']
        result = NAMaintenance.objects.DeleteData(idapp)
        statusResp = 200
        if result == 'Lost':
            statusResp = 500
        return HttpResponse(result,status=statusResp)
def SearchGoodsbyForm(request):
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    goodsFilter = request.GET.get('goods_filter')
    Ilimit = request.GET.get('rows', '')
    NAData = NAMaintenance.objects.search_M_ByForm(goodsFilter)
    if NAData == []:
        results = {"page": "1","total": 0 ,"records": 0,"rows": [] }
    else:
        totalRecord = len(NAData)
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
            datarow = {"id" :str(row['idapp']) +'_fk_goods', "cell" :[row['idapp'],i,row['itemcode'],row['goods'],row['condition'],\
                row['still_guarantee'],row['serialnumber'],row['minus']]}
            rows.append(datarow)
        results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
    return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')

def get_GoodsData(request):
    if request.method == 'GET':
        idapp = request.GET['idapp']
        result = NAMaintenance.objects.getGoods_data(idapp)
        statusResp = 200
        if result == 'HasExist':
            statusResp = 403
            result = 'This data has Exist'
        return HttpResponse(json.dumps(result[0]),status=statusResp,content_type='application/json')
