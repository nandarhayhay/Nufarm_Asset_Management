from django.shortcuts import render
from NA_Models.models import Employee, NASuplier,LogEvent
from django.http import JsonResponse, HttpResponse
from django.core.mail import EmailMessage, BadHeaderError
from django.conf import settings
from smtplib import SMTPException
import datetime
def NA_EmailData(request):
    if request.method == "POST":
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        getUser = request.user.username
        to = request.POST.get('to', '')
        type_report = request.POST['type_report']
        if subject and message and to:
            try:
                email = EmailMessage(
                    subject=subject,
                    body="<"+str(getUser)+">" + message,
                    from_email=getUser,
                    to=[to]
                    )
                import glob
                for name in glob.glob(settings.STATIC_ROOT + '/app/Upload/email_data/'+getUser+'/*'): #get all file in his/her directory
                    email.attach_file(name)
                try:
                    email.send()
                except SMTPException as e:
                    return HttpResponse(e, status=403)
                else:
                    result_all = {}
                    if type_report == 'tabular_data':
                        data_report_tabular = request.POST['data_report_tabular']
                        if 'Employee' in data_report_tabular.split(','):
                            total_empl = Employee.objects.count()
                            result_all['tabular_data_employee'] = str(total_empl) + ' Employees' if total_empl > 1 else str(total_empl) + ' Employee'
                        if 'Suplier' in data_report_tabular.split(','):
                            total_supl = NASuplier.objects.count()
                            result_all['tabular_data_suplier'] = str(total_supl) + ' Supliers' if total_supl > 1 else str(total_supl) + ' Suplier'
                    elif type_report == 'biodata':
                        data_report_empl = request.POST['data_report_empl']
                        data_report_supl = request.POST['data_report_supl']
                        len_report_empl = int(len(data_report_empl.split(',')))
                        len_report_supl = int(len(data_report_supl.split(',')))
                        if data_report_empl != 'none':
                            result_empl = []
                            if len_report_empl > 1:
                                bio_empl = Employee.objects.filter(idapp__in=(data_report_empl.split(',')))\
                                    .values('idapp', 'nik', 'employee_name', 'typeapp', 'jobtype', 'gender', 'status', 'telphp', 'territory', 'descriptions','inactive')
                            elif len_report_empl == 1:
                                bio_empl = Employee.objects.retriveData(data_report_empl)\
                                    .values('idapp', 'nik', 'employee_name', 'typeapp', 'jobtype', 'gender', 'status', 'telphp', 'territory', 'descriptions','inactive')
                            for i in bio_empl:
                                result_empl.append(i)
                            result_all['bio_employee'] = result_empl
                        if data_report_supl != 'none':
                            result_supl = []
                            if len_report_supl > 1:
                                bio_supl = NASuplier.objects.filter(supliercode__in=(data_report_supl.split(',')))\
                                    .values('supliercode', 'supliername', 'address', 'telp', 'hp', 'contactperson','inactive')
                            elif len_supl_empl == 1:
                                bio_supl = NASuplier.objects.retriveData(data_report_supl)\
                                    .values('supliercode', 'supliername', 'address', 'telp', 'hp', 'contactperson','inactive')
                            for i in bio_supl:
                                result_supl.append(i)
                            result_all['bio_suplier'] = result_supl

                    LogEvent.objects.create(nameapp='Send Email', typeapp='P', descriptionsapp={
                            'emailData':[
                                to,
                                getUser,
                                subject,
                                message,
                                'Tabular Data' if type_report == 'tabular_data' else 'Biodata',
                                result_all
                                ]
                            }, createdby=str(request.user.username))

                import os
                for name in glob.glob(settings.STATIC_ROOT + '/app/Upload/email_data/'+getUser+'/*.pdf'):
                    os.remove(name)
            except BadHeaderError: #Preventing header injection from hacker(commonly called HAKEL) SHIT .. .
                return HttpResponse('Invalid header found.')
        return HttpResponse('Success !!!')
    return render(request, 'app/MasterData/NA_F_EmailData.html')

def searchBiodata(request):
    if request.is_ajax():
        q = request.POST['term']
        is_empl = request.POST['is_empl']
        is_supl = request.POST['is_supl']
        get_empl = Employee.objects.filter(employee_name__icontains=q).values('idapp','nik','employee_name')
        get_supl = NASuplier.objects.filter(supliername__icontains=q).values('supliercode', 'supliername')
        result = []
        if is_empl and is_supl:
            if is_empl == 'true':
                for i in get_empl:
                    data = {}
                    data['value'] = str(i['idapp']) + '-employee'
                    data['label'] = i['employee_name']
                    data['nik'] = i['nik']
                    result.append(data)
            
            if is_supl == 'true':
                for j in get_supl:
                    data = {}
                    data['value'] = j['supliercode'] + '-suplier'
                    data['label'] = j['supliername']
                    result.append(data)
    else:
        result = 'failed'
    return JsonResponse(result, safe=False)

def NA_Email_retriveBio(request):
    if request.method == "POST":
        toPDF_type = request.POST['toPDF_type']
        if toPDF_type == 'biodata':
            biodata = {}
            total_bioEmpl = request.POST['total_bioEmpl']
            if int(total_bioEmpl) > 0:
                retrive_Empl = request.POST['bio_empl_idapp']
                if int(total_bioEmpl) > 1:
                    retrive_bioEmplArr = retrive_Empl.split(',')
                    bio_Empl = []
                    get_bioEmpls = Employee.objects.filter(idapp__in=(retrive_bioEmplArr))\
                        .values('idapp', 'nik', 'employee_name', 'typeapp', 'jobtype', 'gender', 'status', 'telphp', 'territory', 'descriptions')
                    for i in get_bioEmpls:
                        bio_Empl.append(i)
                    
                elif int(total_bioEmpl) == 1:
                    bio_Empl = []
                    get_bioEmpl = Employee.objects.retriveData(retrive_Empl)\
                        .values('nik', 'employee_name', 'typeapp', 'jobtype', 'gender', 'status', 'telphp', 'territory', 'descriptions')
                    for i in get_bioEmpl:
                        bio_Empl.append(i)
                biodata['employee'] = bio_Empl
            total_bioSupl = request.POST['total_bioSupl']
            if int(total_bioSupl) > 0:
                retrive_bioSupl = request.POST['bio_supliercode']
                bio_Supl = []
                if int(total_bioSupl) > 1:
                    retrive_bioSuplArr = retrive_bioSupl.split(',')
                    get_bioSupl = NASuplier.objects.filter(supliercode__in=(retrive_bioSuplArr))\
                        .values('supliercode', 'supliername', 'address', 'telp', 'hp', 'contactperson')
                elif int(total_bioSupl) == 1:
                    get_bioSupl = NASuplier.objects.retriveData(retrive_bioSupl)\
                        .values('supliercode', 'supliername', 'address', 'telp', 'hp', 'contactperson')
                for i in get_bioSupl:
                    bio_Supl.append(i)
                biodata['suplier'] = bio_Supl     
    return JsonResponse(biodata)

def NA_EmailUplData(request):
    dir_emailData = settings.STATIC_ROOT+'/app/Upload/email_data/' + str(request.user.username)
    import base64
    try:
        import os, errno
        os.makedirs(dir_emailData, exist_ok=True) #each user must be create directory with his/her name, for handling conflict file .. .
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    is_empl = request.POST['is_empl']
    is_supl = request.POST['is_supl']
    
    if is_empl == 'true':
        toPDF_empl = request.POST['toPDF_empl']
        if toPDF_empl != 'none':
            save_empl = open(dir_emailData + '/Report Employee By %s.pdf' % request.user.username, 'wb')
            save_empl.write(base64.b64decode(toPDF_empl))
            save_empl.close()
    if is_supl == 'true':
        toPDF_supl = request.POST['toPDF_supl']
        if toPDF_supl != 'none':
            save_supl = open(dir_emailData + '/Report Suplier By %s.pdf' % request.user.username, 'wb')
            save_supl.write(base64.b64decode(toPDF_supl))
            save_supl.close()
    return HttpResponse('Success')