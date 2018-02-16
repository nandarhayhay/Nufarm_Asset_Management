from .NA_To_Grids import NA_SuplierGrid
from django.shortcuts import render
from NA_Models.models import NASuplier, LogEvent
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import datetime
from NA_DataLayer.common import CriteriaSearch
from NA_DataLayer.common import ResolveCriteria
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import json
from django.core.serializers.json import DjangoJSONEncoder

@login_required
def NA_Suplier(request):
    return render(request, 'app/MasterData/NA_F_Suplier.html')

def NA_SuplierGetData(request):
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
        suplData = NASuplier.objects.PopulateQuery(IcolumnName,IvalueKey,criteria,dataType).order_by('-' + str(Isidx))
    else:
        suplData = NASuplier.objects.PopulateQuery(IcolumnName,IvalueKey,criteria,dataType)			

    totalRecord = suplData.count()
    paginator = Paginator(suplData, int(Ilimit)) 
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
        datarow = {"id" :row['supliercode'], "cell" :[row['supliercode'],row['supliername'],row['address'],row['telp'],row['hp'],row['contactperson'], \
		    row['inactive'],row['createddate'],row['createdby']]}
        rows.append(datarow)
    results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
    return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')

from django import forms
class NA_Suplier_form(forms.Form):
    supliercode = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class':'NA-Form-Control', 'placeholder':'Enter Suplier Code'
        }))
    supliername = forms.CharField(max_length=40, required=True, widget=forms.TextInput(attrs={
        'class':'NA-Form-Control', 'placeholder':'Enter Suplier Name'
        }))
    address = forms.CharField(max_length=200, required=True, widget=forms.Textarea(attrs={
        'class':'NA-Form-Control', 'placeholder':'Address of Suplier','cols':'100','rows':'2', 'style':'height: 50px;clear:left;width:420px;max-width:420px'
        }))
    telp = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class':'NA-Form-Control', 'placeholder':'Jobtype'
        }))
    hp = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class':'NA-Form-Control', 'placeholder':'Phone Number'
        }))
    contactperson = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class':'NA-Form-Control', 'placeholder':'Contact Person'
        }))
    inactive = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    window_status = forms.CharField(widget=forms.HiddenInput(), required=False)
    initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)
    class Meta:
        model = NASuplier
        exclude = ('createdby','createddate','modifiedby','modifieddate')

def getCurrentUser(request):
    return str(request.user.username)

def getData(request, form):
    clData = form.cleaned_data
    data = {
        'supliercode': clData['supliercode'],
        'supliername': clData['supliername'],
        'address': clData['address'],
        'telp':clData['telp'],
        'hp':clData['hp'],
        'contactperson':clData['contactperson'],
        'inactive':clData['inactive'],
        'createddate':datetime.datetime.now(),
        'createdby': getCurrentUser(request)
        }
    return data

def EntrySuplier(request):
    if request.method == 'POST':
        form = NA_Suplier_form(request.POST)
        if form.is_valid():
            mode = request.POST['mode']
            data = getData(request, form)
            if mode == 'Add':
                checkExist = NASuplier.objects.dataExist(data['supliercode'])
                if checkExist:
                    return JsonResponse({'message':'This data has exists'})
                else:
                   result = NASuplier.objects.create_suplier(**data)
                   return HttpResponse(json.dumps({'message':result}), content_type='application/json')
                   #get idapp for highlight element
            elif mode == 'Edit':
                getSupCode = request.POST['supliercode']
                data['supliercode'] = getSupCode
                data['modifieddate'] = datetime.datetime.now()
                data['modifiedby'] = getCurrentUser(request)
                NASuplier.objects.update_suplier(**data)
                return HttpResponse(json.dumps({'message':data['supliercode']}), content_type='application/json')
            elif mode == 'Open':
                if request.POST['supliername']:
                    return HttpResponse(json.dumps({'messages':'You\'re try to Edit this Data with Open Mode\nWith technic inspect element\nWhat dou you think about Programmer ? :D'}))
            elif mode == 'Delete':
                getSupCode = request.POST['supliercode']
                NASuplier.objects.delete_suplier(getSupCode)
        return HttpResponse(json.dumps({'message':'success'}), content_type='application/json')
    elif request.method == 'GET':
        getSupCode = request.GET['supliercode']
        mode = request.GET['mode']
        if mode == 'Edit' or mode == 'Open':
            result = NASuplier.objects.retriveData(getSupCode)[0]
            data = {
            #'idapp':result.idapp,
            'supliercode':result.supliercode,
            'supliername':result.supliername,
            'address':result.address,
            'telp':result.telp,
            'hp':result.hp,
            'contactperson':result.contactperson,
            'inactive':result.inactive
            }
            form = NA_Suplier_form(initial=data)
        else:
            form = NA_Suplier_form()
        return render(request, 'app/MasterData/EntrySuplier.html', {'form':form})


def ShowCustomFilter(request):
	if request.is_ajax():
		cols = []
		cols.append({'name':'supliercode','value':'supliercode','selected':'','dataType':'varchar','text':'Suplier Code'})
		cols.append({'name':'supliername','value':'supliername','selected':'True','dataType':'varchar','text':'Suplier Name'})
		cols.append({'name':'address','value':'address','selected':'','dataType':'varchar','text':'Address'})
		cols.append({'name':'telp','value':'telp','selected':'','dataType':'varchar','text':'Telp'})
		cols.append({'name':'hp','value':'hp','selected':'','dataType':'varchar','text':'Hp'})
		cols.append({'name':'contactperson','value':'contactperson','selected':'','dataType':'varchar','text':'Contact Person'})
		cols.append({'name':'inactive','value':'inactive','selected':'','dataType':'boolean','text':'InActive'})
		return render(request, 'app/UserControl/customFilter.html', {'cols': cols})	

def retriveSuplier(request):
    if request.method == 'POST':
        get_supliercode = request.POST['supliercode']
        result = NASuplier.objects.get(supliercode=get_supliercode)
        data = {
        'supliercode':result.supliercode,
        'supliername':result.supliername,
        'address':result.address,
        'telp':result.telp,
        'hp':result.hp,
        'contactperson':result.contactperson,
        'inactive':result.inactive,
        }
    return JsonResponse(data, safe=False)


def NA_Suplier_delete(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            if request.POST['oper'] == 'del':
                get_supcode = request.POST.get('supliercode')
                log_supl_deleted = NASuplier.objects.retriveData(get_supcode).values('supliercode', 'supliername',\
                    'address', 'telp', 'hp', 'contactperson', 'inactive', 'createddate', 'createdby')[0]
                LogEvent.objects.create(nameapp='Deleted Suplier',typeapp='P', descriptionsapp={
                    'deleted':[
                        log_supl_deleted['supliercode'],
                        log_supl_deleted['supliername'],
                        log_supl_deleted['address'],
                        log_supl_deleted['telp'],
                        log_supl_deleted['hp'],
                        log_supl_deleted['contactperson'],
                        log_supl_deleted['inactive'],
                        log_supl_deleted['createddate'].strftime('%d %B %Y %H:%M:%S'),
                        log_supl_deleted['createdby']
                        ]
                    }, createdby=str(request.user.username))
                NASuplier.objects.delete_suplier(get_supcode)

    return HttpResponse('success')