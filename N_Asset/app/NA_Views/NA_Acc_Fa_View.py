from django.shortcuts import render
from NA_Models.models import NAAccFa, goods
from django import forms
from django.http import HttpResponse, JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from NA_DataLayer.common import CriteriaSearch, ResolveCriteria, commonFunct
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import datetime
#from dateutil import relativedelta
from decimal import Decimal
def NA_AccGetData(request):
    IcolumnName = request.GET.get('columnName')
    IvalueKey =  request.GET.get('valueKey')
    IdataType =  request.GET.get('dataType')
    Icriteria =  request.GET.get('criteria')
    Ilimit = request.GET.get('rows', '')
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    Ipage = request.GET.get('page')
    getColumn = commonFunct.retriveColumn(table=[NAAccFa,goods],resolve=IcolumnName,initial_name=['ac','g'])
    criteria = ResolveCriteria.getCriteriaSearch(str(Icriteria))
    dataType = ResolveCriteria.getDataType(str(IdataType))
    accData = NAAccFa.objects.PopulateQuery(getColumn,IvalueKey,criteria,dataType,Isidx,Isord)
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
        datarow = {"id" :row['idapp'], "cell" :[row['idapp'],i,row['goods'],row['itemcode'],row['serialnumber'],row['year'],\
            row['startdate'],row['depr_expense'],row['depr_accumulation'],row['bookvalue'],row['createddate'],row['createdby']]}
        rows.append(datarow)
    results = {"page": dataRows.number,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
    return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')


class NA_Acc_Form(forms.Form):
    fk_goods = forms.CharField(required=True,widget=forms.HiddenInput())
    itemcode = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','placeholder':'Item code','style':'width:120px'}),label='Search goods')
    goods_name = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','disabled':'disabled','placeholder':'Goods Name','style':'width:150px'}))
    brandname = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','disabled':'disabled','placeholder':'Brand Name','style':'width:155px'}))
    typeApp = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','disabled':'disabled','placeholder':'Type of goods','style':'width:155px'}))
    serialNumber = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','disabled':'disabled','placeholder':'Serial Number','style':'width:225px'}))
    year = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','disabled':'disabled','placeholder':'Year','style':'width:110px'}))
    startdate = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','disabled':'disabled','placeholder':'Start Date','style':'width:115px'}))
    enddate = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','disabled':'disabled','placeholder':'End Date','style':'width:115px'}))
    depr_expense = forms.DecimalField(required=False,label='Depreciation Expense',widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','disabled':'disabled','placeholder':'Depreciation Expense','style':'width:227px'}))
    depr_accumulation = forms.DecimalField(required=False,label='Depreciation Accumulation',widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','disabled':'disabled','placeholder':'Depreciation Accumulation','style':'width:220px'}))
    bookvalue = forms.DecimalField(required=False,label='Book Value',widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','disabled':'disabled','placeholder':'Book Value','style':'width:250px'}))
    depr_method = forms.CharField(disabled=True,label='Depreciation Method',required=False,widget=forms.TextInput(attrs={
                'class':'NA-Form-Control','placeholder':'Depreciation Method','style':'width:225px'}))
    price = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','disabled':'disabled','placeholder':'Price of goods','style':'width:236px'}))
    economiclife = forms.CharField(required=True,label='Economic Life',widget=forms.TextInput(attrs={
        'class':'NA-Form-Control','disabled':'disabled','placeholder':'Economic Life','style':'width:120px'}))
    initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)

def NA_Acc_FA(request):
    return render(request,'app/MasterData/NA_F_Acc_FA.html')

def getData(request, forms):
    clData = forms.cleaned_data
    data = {
        'fk_goods': clData['fk_goods'],'goods_name': clData['goods_name'],'typeApp':clData['typeApp'],
        'serialNumber':clData['serialNumber'],'year': clData['year'],'startdate': clData['startdate'],
        'enddate':clData['enddate'],'depr_expense': clData['depr_expense'],
        'depr_accumulation': clData['depr_accumulation'],'bookvalue': clData['bookvalue'],
        'depr_method':clData['depr_method'],'price':clData['price'],'economiclife':clData['economiclife']
        }
    return data

def EntryAcc(request):
    if request.method == 'POST':
        form = NA_Acc_Form(request.POST)
        if form.is_valid():
            data = getData(request,form)
            if request.POST['mode'] == 'Add':
                createdby = str(request.user.username)
                fk_goods = data['fk_goods']
                #year = Decimal(data['year']) #sisa umur economic
                economiclife = Decimal(data['economiclife']) #original economic
                startdate = datetime.datetime.strptime(data['startdate'],'%d/%m/%Y').date()
                startdate = startdate.strftime('%Y-%m-%d')
                price = Decimal(data['price'])
                depr_method = lambda dm: 'SL' if dm == 'Straight Line' else('DDB' if dm == 'Double Declining Balance' else 'STYD')
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                values_insert = []
                def settings_generate(opt):
                    settings = {'month_of':opt['month_of'],'economiclife':economiclife,'typeApp':data['typeApp'],
                                'serialNumber':data['serialNumber'],'price':price,'depr_method':depr_method(data['depr_method']),
                                'depr_expense':opt['depr_Expense'],'startdate':startdate,'fk_goods': fk_goods,'createddate':now,
                                'createdby':createdby}
                    if opt['depr_method'] == 'STYD':
                        settings['depr_acc'] = opt['depr_acc']
                    return settings

                if depr_method(data['depr_method']) == 'SL' or depr_method(data['depr_method']) == 'DDB':
                    depr_expense = price/(economiclife*12)
                    for i in range(int(economiclife*12) + 1):
                        generate_acc(settings_generate({
                            'depr_method':'SL','month_of':i,'depr_Expense':depr_expense
                            }),values_insert)
                elif depr_method(data['depr_method']) == 'STYD':
                    arr_year = [i for i in range(int(economiclife),0,-1)]
                    total_year = 0
                    for i in arr_year:
                        total_year+=i
                    arr_depr_expense = [int(i/total_year*int(price)) for i in arr_year] #per tahun
                    depr_acc = 0
                    month_of = 0
                    generate_acc(settings_generate({
                        'depr_method':'STYD',
                        'depr_acc':Decimal('0.00'),'depr_Expense':Decimal(arr_depr_expense[0]/12),'month_of':0
                        }),values_insert)
                    for i in arr_depr_expense:
                        for j in range(1,13):
                            depr_acc+=Decimal(i/12)
                            month_of +=1
                            generate_acc(settings_generate({
                                'depr_method':'STYD',
                                'depr_acc':depr_acc,'depr_Expense':Decimal(i/12),'month_of':month_of
                                }),values_insert)
                str_values = ','.join(values_insert)
                result = NAAccFa.objects.create_acc_FA(str_values)
                statusResp = 200
                message = 'success'
                if result != 'success':
                    statusResp = 403
                    message = 'Fail'
                return HttpResponse(message,status=statusResp)
            elif request.POST['mode'] == 'Edit':
                pass
            elif request.POST['mode'] == 'Open':
                pass
            return HttpResponse('success')
    elif request.method == 'GET':
        mode = request.GET['mode']
        if mode == 'Open':
            idapp = request.GET['idapp']
            result = NAAccFa.objects.retriveData(idapp)[0]
            result['startdate'] = result['startdate'].strftime('%d %B %Y')
            result['enddate'] = result['enddate'].strftime('%d %B %Y')
            form = NA_Acc_Form(initial=result)
            form.fields['itemcode'].label = 'Item code'
            form.height = '280px'
        else:
            form = NA_Acc_Form()
            del form.fields['depr_expense'], form.fields['depr_accumulation'],form.fields['bookvalue'], form.fields['year']
            form.fields['price'].widget.attrs['style'] = 'width:225px'
            form.fields['serialNumber'].widget.attrs['style'] = 'width:190px'
            form.fields['price'].widget.attrs['style'] = 'width:155px'
            form.fields['startdate'].widget.attrs['style'] = 'width:120px'
            form.fields['enddate'].widget.attrs['style'] = 'width:155px'
            form.fields['depr_method'].widget.attrs['style'] = 'width:190px'
            form.height = '210px'
        return render(request,'app/MasterData/NA_Entry_AccFA.html',{'form':form,'mode':mode})
def ShowCustomFilter(request):
	if request.is_ajax():
		cols = []
		cols.append({'name':'goodsname','value':'goodsname','selected':'True','dataType':'varchar','text':'Goods Name'})
		cols.append({'name':'brandname','value':'brandname','selected':'','dataType':'varchar','text':'Brand Name'})
		cols.append({'name':'itemcode','value':'itemcode','selected':'','dataType':'varchar','text':'Item code'})
		cols.append({'name':'serialnumber','value':'serialnumber','selected':'','dataType':'varchar','text':'Serial Number'})
		cols.append({'name':'year','value':'year','selected':'','dataType':'decimal','text':'Year'})
		cols.append({'name':'startdate','value':'startdate','selected':'','dataType':'varchar','text':'Start Date'})
		cols.append({'name':'depr_expense','value':'depr_expense','selected':'','dataType':'decimal','text':'Depreciation Expense'})
		cols.append({'name':'depr_accumulation','value':'depr_accumulation','selected':'','dataType':'decimal','text':'Depreciation Accumulation'})
		cols.append({'name':'bookvalue','value':'bookvalue','selected':'','dataType':'decimal','text':'Book Value'})
		return render(request, 'app/UserControl/customFilter.html', {'cols': cols})

def generate_acc(acc,values_insert):
    month_of = acc['month_of']
    price = acc['price']
    typeApp = acc['typeApp']
    serialNumber = acc['serialNumber']
    depr_method = acc['depr_method']
    startdate = acc['startdate']
    depr_expense = Decimal(acc['depr_expense'])
    economiclife = acc['economiclife']
    if month_of == 0:
        str_values = ['("'+str(acc['fk_goods']),str(serialNumber),str(typeApp),str(economiclife),str(startdate),str(depr_expense),
                      '0.00',str('%0.2f' % price),acc['createddate'],acc['createdby']+'")']
    else:
        total_rows = int(economiclife*12)
        if depr_method == 'SL' or depr_method == 'DDB':
            if depr_method == 'SL':
                depr_accumulation = depr_expense*month_of
            elif depr_method == 'DDB':
                depr_accumulation = 2*(depr_expense*month_of)
        elif depr_method == 'STYD':
            depr_accumulation = acc['depr_acc']
        residue_eccLife = economiclife*(total_rows-month_of)/total_rows
        if residue_eccLife == 0:
            bookvalue = 0
            depr_accumulation = price
        else:
            bookvalue = price - depr_accumulation
        str_values = ['("'+str(acc['fk_goods']),str(serialNumber),str(typeApp),str('%0.2f' % residue_eccLife),str(startdate),str('%0.2f' % depr_expense),\
            str('%0.2f' % depr_accumulation),str('%0.2f' % bookvalue),acc['createddate'],acc['createdby']+'")']
    str_values = '","'.join(str_values)
    return values_insert.append(str_values)#(FK_Goods,Goods_Name,Year,StartDate,Depr_Expense,Depr_Accumulation,BookValue,CreatedDate,CreatedBy)
def getGoods_data(request):
    if request.is_ajax() and request.method == 'GET':
        idapp = request.GET['idapp']
        goods_obj = NAAccFa.objects.getGoods_data(idapp)[0]
        depr_method = lambda dm: 'Straight Line Method' if dm == 'SL'\
            else('Double Declining Balance' if dm == 'DDB' else 'Sum of The Year Digit')
        goods_obj['startdate'] = goods_obj['startdate'].strftime('%d/%m/%Y')
        goods_obj['enddate'] = goods_obj['enddate'].strftime('%d/%m/%Y')
        goods_obj['depr_method'] = depr_method(goods_obj['depr_method'])
        #data = {'goods_name':goods_obj.goodsname,'brandname':goods_obj.brandname,'price':goods_obj.price_label,
        #        'startdate':goods_obj.startdate.strftime('%d %b %Y'),'enddate':goods_obj.enddate.strftime('%d %b %Y'),
        #        '_price':goods_obj.price_orig,'depr_method':depr_method(goods_obj.depr_method),
        #        'economiclife':goods_obj.economiclife,'serialNumber':goods_obj.serialnumber,'typeApp':goods_obj.typeapp}
        return HttpResponse(json.dumps(goods_obj, cls=DjangoJSONEncoder),content_type='application/json')

def SearchGoodsbyForm(request):
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    goodsFilter = request.GET.get('goods_filter')
    Ilimit = request.GET.get('rows', '')
    NAData = NAAccFa.objects.searchAcc_ByForm(goodsFilter)
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
            datarow = {"id" :str(row['idapp']) +'_fk_goods', "cell" :[row['idapp'],i,row['itemcode'],row['goods'],row['serialnumber']]}
            rows.append(datarow)
        results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
    return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')