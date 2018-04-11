from django.http import HttpResponse, JsonResponse
from NA_Models.models import LogEvent
from django.db import connection, transaction
import json
import datetime

def NA_LogEvent_data(request):
    LogEvent_data = []
    tahun = []
    bulan = []
    hari = []
    ev = LogEvent.objects.filter(createdby=request.user.username).values('nameapp', 'createddate')
    is_filter = request.GET.get('_Search')
    must_filter = False
    if is_filter is not None:
        must_filter = True
    if must_filter:
        filter_log = request.GET['search']
        ev = ev.filter(nameapp__icontains=filter_log)
    if ev.exists():
        event = [i for i in ev.iterator()] #get log event filter by user
        get_dyn_year = [i for i in ev.dates('createddate', 'year', order='DESC').iterator()] #get dynamic year
        get_dyn_month = [i for i in ev.dates('createddate', 'month', order='DESC').iterator()] #get dynamic month
        get_dyn_day = [i for i in ev.dates('createddate', 'day', order='DESC').iterator()] #get dynamic day
        for y in get_dyn_year:
            tahun.append(y)
        for m in get_dyn_month:
            bulan.append(m)
        for d in get_dyn_day:
            hari.append(d)
        result = []
        for t in tahun:
          for b in bulan:
              if b.year == t.year:
                result.append((str(t.year),b.strftime("%B %Y"))) #b.strftime for returning unique text e.g: December 2017 , if the text is December only .. the date of 2018 may be have this children (atau bisa disebut Bentrok) :D
        for b in bulan:
          for h in hari:
              if h.year == b.year and h.month == b.month:
                result.append((b.strftime("%B %Y"),h))
        for h in hari:
          for e in event:
              if e['createddate'].year == h.year and e['createddate'].month == h.month and e['createddate'].day == h.day:
                result.append((h,'{} at {}'.format(e['nameapp'] , e['createddate'].strftime("%H:%M:%S"))))
        parents, children = zip(*result) #get parent and children then return tuple within list .. . :D
        root_nodes = {x for x in parents if x not in children}
        getUser = str(request.user.username)
        for node in root_nodes:
          result.append((getUser, node))
        result.append(('Log Event', getUser))
        def get_nodes(node):
            data = {}
            data['text'] = node
            if data['text'] == str(request.user.username):
                data['iconCls'] = 'fa fa-user'
            if must_filter:
                data['state'] = 'Open'
            children = get_children(node)
            if children:
                data['children'] = [get_nodes(child) for child in children]
            return data

        def get_children(node):
            return [x[1] for x in result if x[0] == node]

        log = get_nodes('Log Event')
        LogEvent_data.append(log)

    else:
        LogEvent_data = []

    def convert(o):
        if isinstance(o, datetime.date):
            return '{} {} {}'.format(o.strftime('%d'), o.strftime('%B'), o.strftime('%Y'))
    return HttpResponse(json.dumps(LogEvent_data, indent=4, default=convert))

def LogDescriptions(request):
    if request.method == 'GET':
        Createddate = request.GET.get('createddate')
        data = LogEvent.objects.filter(createddate=Createddate,createdby=request.user.username).values('descriptions')[0]['descriptions']
    return HttpResponse(json.dumps([data]), content_type='application/json')
