from django.http import HttpResponse, JsonResponse
from NA_Models.models import LogEvent
from django.db import connection, transaction
import json
import datetime
#from app.middleware import get_current_user
def line_profiler(view=None, extra_view=None):
    import line_profiler

    def wrapper(view):
        def wrapped(*args, **kwargs):
            prof = line_profiler.LineProfiler()
            prof.add_function(view)
            if extra_view:
                [prof.add_function(v) for v in extra_view]
            with prof:
                resp = view(*args, **kwargs)
            prof.print_stats()
            return resp
        return wrapped
    if view:
        return wrapper(view)
    return wrapper

@line_profiler
def NA_LogEvent_data(request):
    LogEvent_data = []
    tahun = []
    bulan = []
    hari = []
    ev = LogEvent.objects.filter(createdby=request.user.username).values('nameapp', 'createddate')
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

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
    dict(zip(columns, row))
    for row in cursor.fetchall()
]

@line_profiler
def LogDescriptions(request):
    if request.method == 'GET':
        get_desc = request.GET.get('createddate')
        #type_log = request.GET['type_log']
        #tbl_log = request.GET['tbl_log']
        #I_gender = None
        #I_status = None
        #I_inactive = None
        #if type_log == 'created':
        #    if tbl_log == 'employee':
        #        I_gender = 4
        #        I_status = 5
        #        I_inactive = 9
        #cursor = connection.cursor()
        #with transaction.atomic():
        #    label = '''SELECT IDApp,IF(json_extract(descriptionsapp,"$.created[4]")="M",json_replace(descriptionsapp,"$.created[4]","Male"),
        #    IF(json_extract(descriptionsapp,"$.createddate[4]")="F",json_replace(descriptionsapp,"$.created[4]","Female"),"$.created[4]")) AS
        #    descriptionsapp FROM LogEvent WHERE createddate=%(createddate)s AND createdby=%(createdby)s'''
        #    prms = {
        #        'createddate':get_desc,
        #        'createdby':request.user.username
        #        }
        #    cursor.execute(label,prms)
        #    row = dictfetchall(cursor)
        by_user = LogEvent.objects.raw('''SELECT IDApp,descriptionsapp FROM LogEvent WHERE createddate=%s AND createdby=%s''',[get_desc,request.user.username])
        #by_user = LogEvent.objects.filter(createdby=request.user.username).values('descriptionsapp')
        #get_createddate = by_user.filter(createddate = get_desc).iterator()
        data = [
         i.__get_descriptions__() for i in by_user
        ]
    return HttpResponse(json.dumps(data), content_type='application/json')