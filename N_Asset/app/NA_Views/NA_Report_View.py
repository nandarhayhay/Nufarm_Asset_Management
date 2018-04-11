#from io import BytesIO
#from reportlab.pdfgen import canvas
#from django.http import HttpResponse
#from django.conf import settings
#from NA_Models.models import Employee
#from reportlab.lib import colors
#from reportlab.lib.pagesizes import letter
#from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
#def write_pdf_view(request):
#    response = HttpResponse(content_type='application/pdf')
#    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

#    buffer = BytesIO()
#    #p = canvas.Canvas(buffer)

#    ## Start writing the PDF here
#    #dir_image = settings.BASE_DIR + '/app/static/app/images/NufarmLogo2.jpg'
#    #p.drawImage(dir_image,15,730,100,100)

 
#    doc = SimpleDocTemplate(settings.BASE_DIR + '/app/static/app/Upload/Template_Report.pdf')
#    # container for the 'Flowable' objects
#    elements = []
 
#    data= [['00', '01', '02', '03', '04'],
#           ['10', '11', '12', '13', '14'],
#           ['20', '21', '22', '23', '24'],
#           ['30', '31', '32', '33', '34']]
#    t=Table(data)
#    t.setStyle(TableStyle([('BACKGROUND',(1,1),(-2,-2),colors.green),
#                           ('TEXTCOLOR',(0,0),(1,-1),colors.red)]))
#    elements.append(t)
#    # write the document to disk
#    doc.build(elements)

#    #thead = ['Nik','Employee Name']
#    #data = Employee.objects.all().values('nik','employee_name')
#    #tbody = [i for i in data]
#    #for i in range(len(thead)):
#    #    p.drawString(15 + (i*30),680,thead[i])
#    #    for j in range(len(tbody)):
#    #        p.drawString(15,650-(j*30),tbody[j]['nik'])
#    # End writing

#    #p.showPage()
#    #p.save()

    
#    #canvas = doc.canv(buffer)
#    #pdf = buffer.getvalue()
#    #buffer.close()
#    pdf = open(settings.BASE_DIR + '/app/static/app/Upload/Template_Report.pdf','r')
#    response.write(pdf)
#    return response