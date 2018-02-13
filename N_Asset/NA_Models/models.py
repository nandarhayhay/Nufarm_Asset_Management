from django.db import models
from datetime import datetime
from NA_DataLayer.NA_Goods_BR import NA_BR_Goods,CustomManager
from NA_DataLayer.NA_Goods_Receive_BR import NA_BR_Goods_Receive,CustomSuplierManager,custEmpManager
#from django_mysql.models import JSONField

#class NABRGoods(models.Manager):
#	def serchData(columKey='',valueKey=''):
#		return super.get_queryset(NABRGoods,self).filter(columKey=valueKey)

#class LogEvent(models.Model):
#    idapp = models.AutoField(db_column='IDApp', primary_key=True)
#    nameapp = models.CharField(db_column='NameApp', max_length=30)
#    typeapp = models.CharField(db_column='TypeApp', max_length=10)
#    descriptionsapp = JSONField()
#    createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
#    createdby = models.CharField(db_column='CreatedBy', max_length=30)

#    def __str__(self):
#        return '{}'.format(self.nameapp)

#    class Meta:
#        db_table = 'LogEvent'

class Employee(models.Model):
	idapp = models.AutoField(db_column='IDApp', primary_key=True)
	nik = models.CharField(db_column='NIK', max_length=50)
	employee_name = models.CharField(db_column='Employee_Name', max_length=150, blank=True, null=True)
	typeapp = models.CharField(db_column='TypeApp', max_length=1, blank=True, null=True)
	jobtype = models.CharField(db_column='JobType', max_length=150, blank=True, null=True)
	gender = models.CharField(db_column='Gender', max_length=10)
	status = models.CharField(db_column='Status', max_length=1, blank=True, null=True)
	telphp = models.CharField(db_column='TelpHP', max_length=20, blank=True, null=True)
	territory = models.CharField(db_column='Territory', max_length=50, blank=True, null=True)
	descriptions = models.CharField(db_column='Descriptions', max_length=200, blank=True, null=True)
	inactive = models.BooleanField(db_column='InActive', max_length=1)
	createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
	createdby = models.CharField(db_column='CreatedBy', max_length=100)
	modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True, auto_now=True)
	modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)
	def __str__(self):
		return self.employee_name
	class Meta:
		managed = True
		db_table = 'employee'
	customManager = custEmpManager()
    #from NA_DataLayer.NA_Employee import NA_BR_Employee

    #NA = NA_BR_Employee()
    #objects = models.Manager() #default manager


class NAAccFa(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    fk_goods = models.CharField(db_column='FK_Goods', max_length=50)  # Field name made lowercase.
    year = models.DecimalField(db_column='Year', max_digits=10, decimal_places=2)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate')  # Field name made lowercase.
    depr_expense = models.DecimalField(db_column='Depr_Expense', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    depr_accumulation = models.DecimalField(db_column='Depr_Accumulation', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    bookvalue = models.DecimalField(db_column='BookValue', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lastupdated = models.DateTimeField(db_column='LastUpdated', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'n_a_acc_fa'


class NAAppparams(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    codeapp = models.CharField(db_column='CodeApp', max_length=64)  # Field name made lowercase.
    nameapp = models.CharField(db_column='NameApp', max_length=100, blank=True, null=True)  # Field name made lowercase.
    typeapp = models.CharField(db_column='TypeApp', max_length=64, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    valuechar = models.CharField(db_column='ValueChar', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fkidapp = models.SmallIntegerField(db_column='FKIDApp', blank=True, null=True)  # Field name made lowercase.
    fkcodeapp = models.CharField(db_column='FKCodeApp', max_length=64, blank=True, null=True)  # Field name made lowercase.
    attstrparams = models.CharField(db_column='AttStrParams', max_length=20, blank=True, null=True)  # Field name made lowercase.
    attdecparams = models.DecimalField(db_column='AttDecParams', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    valuestrparams = models.CharField(db_column='ValueStrParams', max_length=50, blank=True, null=True)  # Field name made lowercase.
    valuedecparams = models.DecimalField(db_column='ValueDecParams', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    inactive = models.IntegerField(db_column='InActive')  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'n_a_appparams'
        unique_together = (('idapp', 'codeapp'),)


class NADisposal(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    fk_goods = models.CharField(db_column='FK_Goods', max_length=30, blank=True, null=True)  # Field name made lowercase.
    datedisposal = models.DateField(db_column='DateDisposal')  # Field name made lowercase.
    ishasvalue = models.IntegerField(db_column='IsHasValue', blank=True, null=True)  # Field name made lowercase.
    issold = models.IntegerField(db_column='IsSold', blank=True, null=True)  # Field name made lowercase.
    sellingprice = models.DecimalField(db_column='SellingPrice', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    fk_responsible_person = models.CharField(db_column='FK_Responsible_Person', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fk_acc_fa = models.CharField(db_column='FK_Acc_FA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fk_stock = models.IntegerField(db_column='FK_Stock', blank=True, null=True)  # Field name made lowercase.
    bookvalue = models.DecimalField(db_column='BookValue', max_digits=10, decimal_places=4)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'n_a_disposal'


class goods(models.Model):
	idapp = models.AutoField(primary_key=True,db_column='IDApp')  # Field name made lowercase.
	itemcode = models.CharField(db_column='ItemCode', max_length=30)  # Field name made lowercase.
	goodsname = models.CharField(db_column='GoodsName', max_length=150)  # Field name made lowercase.
	brandname = models.CharField(db_column='BrandName', max_length=100)  # Field name made lowercase.
	typeapp = models.CharField(db_column='TypeApp', max_length=32)  # Field name made lowercase.
	priceperunit = models.DecimalField(db_column='PricePerUnit', max_digits=30,decimal_places=4)  # Field name made lowercase.
	depreciationmethod = models.CharField(db_column='DepreciationMethod', max_length=4)  # Field name made lowercase.
	unit = models.CharField(db_column='Unit', max_length=30)  # Field name madelowercase.
	economiclife = models.DecimalField(db_column='EconomicLife', max_digits=10,decimal_places=2)  # Field name made lowercase.
	placement = models.CharField(db_column='Placement', max_length=50, blank=True, null=True)  # Field name made lowercase.
	descriptions = models.CharField(db_column='Descriptions', max_length=150, blank=True, null=True)  # Field name made lowercase.
	inactive = models.BooleanField(db_column='InActive', blank=True, null=True) # Field name made lowercase.
	createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
	createdby = models.CharField(db_column='CreatedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.
	modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
	modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)

	class Meta:
		db_table = 'n_a_goods'
		app_label = ''

	objects =  NA_BR_Goods()
	customs = CustomManager()
#class NAGoods(models.Model):
#    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
#    itemcode = models.CharField(db_column='ItemCode', max_length=30)  # Field name made lowercase.
#    goodsname = models.CharField(db_column='GoodsName', max_length=100)  # Field name made lowercase.
#    brandname = models.CharField(db_column='BrandName', max_length=50, blank=True, null=True)  # Field name made lowercase.
#    typeapp = models.CharField(db_column='TypeApp', max_length=32)  # Field name made lowercase.
#    priceperunit = models.DecimalField(db_column='PricePerUnit', max_digits=10, decimal_places=4)  # Field name made lowercase.
#    depreciationmethod = models.CharField(db_column='DepreciationMethod', max_length=2)  # Field name made lowercase.
#    unit = models.CharField(db_column='Unit', max_length=30)  # Field name made lowercase.
#    economiclife = models.DecimalField(db_column='EconomicLife', max_digits=10, decimal_places=2)  # Field name made lowercase.
#    placement = models.CharField(db_column='Placement', max_length=50, blank=True, null=True)  # Field name made lowercase.
#    descriptions = models.CharField(db_column='Descriptions', max_length=150, blank=True, null=True)  # Field name made lowercase.
#    inactive = models.IntegerField(db_column='InActive', blank=True, null=True)  # Field name made lowercase.
#    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
#    createdby = models.CharField(db_column='CreatedBy', max_length=100)  # Field name made lowercase.
#    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
#    modifiedby = models.CharField(db_column='ModifiedBy', max_length=100)  # Field name made lowercase.

#    class Meta:
#        managed = True
#        db_table = 'n_a_goods'

#    objects =  NA_BR_Goods()
#    def __str__(self):
#        return self.nameApp

class NAGoodsLending(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    fk_goods = models.CharField(db_column='FK_Goods', max_length=30)  # Field name made lowercase.
    fk_employee = models.CharField(db_column='FK_Employee', max_length=50)  # Field name made lowercase.
    datelending = models.DateField(db_column='DateLending', blank=True, null=True)  # Field name made lowercase.
    qty = models.IntegerField(db_column='Qty')  # Field name made lowercase.
    fk_stock = models.CharField(db_column='FK_Stock', max_length=50)  # Field name made lowercase.
    fk_responsible_person = models.CharField(db_column='FK_Responsible_Person', max_length=50, blank=True, null=True)  # Field name made lowercase.
    benefitof = models.CharField(db_column='BenefitOf', max_length=150, blank=True, null=True)  # Field name made lowercase.
    fk_sender = models.CharField(db_column='FK_Sender', max_length=50, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=10, blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'n_a_goods_lending'


class NAGoodsOutwards(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    fk_goods = models.CharField(db_column='FK_Goods', max_length=30)  # Field name made lowercase.
    qty = models.IntegerField(db_column='Qty', blank=True, null=True)  # Field name made lowercase.
    daterequest = models.DateTimeField(db_column='DateRequest')  # Field name made lowercase.
    datereleased = models.DateTimeField(db_column='DateReleased')  # Field name made lowercase.
    fk_employee = models.CharField(db_column='FK_Employee', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fk_usedemployee = models.CharField(db_column='FK_UsedEmployee', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fk_frommaintenance = models.IntegerField(db_column='FK_FromMaintenance', blank=True, null=True)  # Field name made lowercase.
    fk_responsibleperson = models.CharField(db_column='FK_ResponsiblePerson', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fk_sender = models.CharField(db_column='FK_Sender', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fk_stock = models.IntegerField(db_column='FK_Stock', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'n_a_goods_outwards'

class NASuplier(models.Model):
	supliercode = models.CharField(db_column='SuplierCode', primary_key=True, max_length=30)
	supliername = models.CharField(db_column='SuplierName', max_length=100, blank=True, null=True)
	address = models.CharField(db_column='Address', max_length=150, blank=True, null=True)
	telp = models.CharField(db_column='Telp', max_length=20, blank=True, null=True)
	hp = models.CharField(db_column='HP', max_length=20, blank=True, null=True)
	contactperson = models.CharField(db_column='ContactPerson', max_length=100, blank=True, null=True)
	inactive = models.BooleanField(db_column='InActive', max_length=1)
	createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
	createdby = models.CharField(db_column='CreatedBy', max_length=100, blank=True, null=True)
	modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)
	modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)
	def __str__(self):
		return self.supliername
	#from NA_DataLayer.NA_Suplier import NA_BR_Suplier
	#NA = NA_BR_Suplier()
	class Meta:
		managed = False
		db_table = 'n_a_suplier'
		app_label = ''
	objects = models.Manager() #default manager
	customManager = CustomSuplierManager()
class NAGoodsReceive(models.Model):
	idapp = models.AutoField(db_column='IDApp', primary_key=True)
	idapp_fk_goods =models.ForeignKey(goods,db_column='fk_goods')
	datereceived = models.DateTimeField(db_column='DateReceived')
	fk_suplier = models.ForeignKey(NASuplier,db_column='FK_Suplier')
	totalpurchase = models.SmallIntegerField(db_column='TotalPurchase')
	totalreceived = models.SmallIntegerField(db_column='TotalReceived')
	idapp_fk_receivedby = models.ForeignKey(Employee, db_column='FK_ReceivedBy', max_length=50)  # Field name made lowercase.
	idapp_fk_p_r_by = models.ForeignKey(Employee,db_column='FK_P_R_By', max_length=50, blank=True, null=True)
	createddate = models.DateTimeField(db_column='CreatedDate')
	createdby = models.CharField(db_column='Createdby', max_length=50)
	modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)
	modifiedby = models.CharField(db_column='ModifiedBy', max_length=50, blank=True, null=True)
	descriptions =  models.CharField(db_column='Descriptions', max_length=250, blank=True, null=True)# Field name made lowercase.
	descbysystem =  models.CharField(db_column='DescBySystem', max_length=250, blank=True, null=True)# Field name made lowercase.
	class Meta:
		managed = False
		db_table = 'n_a_goods_receive'
		app_label = ''
	objects = NA_BR_Goods_Receive()
	
class NAGoodsReturn(models.Model):
	idapp = models.AutoField(db_column='IDApp', primary_key=True)
	fk_goods = models.ForeignKey(goods, db_column='FK_Goods')
	datereturn = models.DateTimeField(db_column='DateReturn')
	condition = models.CharField(db_column='Condition', max_length=1)
	fk_fromemployee = models.CharField(db_column='FK_FromEmployee', max_length=50, blank=True, null=True)
	fk_usedemployee = models.CharField(db_column='FK_UsedEmployee', max_length=50, blank=True, null=True)
	iscompleted = models.IntegerField(db_column='IsCompleted')
	minus = models.CharField(db_column='Minus', max_length=100, blank=True, null=True)
	fk_goods_lend = models.IntegerField(db_column='FK_Goods_Lend', blank=True, null=True)
	descriptions = models.CharField(db_column='Descriptions', max_length=200, blank=True, null=True)
	createddate = models.DateTimeField(db_column='CreatedDate')
	createdby = models.CharField(db_column='CreatedBy', max_length=100)
	modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)
	modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)
	
	class Meta:
		managed = True
		db_table = 'n_a_goods_return'
		app_label = ''

class NAMaintenance(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    requestdate = models.DateField(db_column='RequestDate', blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate')  # Field name made lowercase.
    isstillguarantee = models.TextField(db_column='IsStillGuarantee')  # Field name made lowercase. This field type is a guess.
    expense = models.DecimalField(db_column='Expense', max_digits=10, decimal_places=4)  # Field name made lowercase.
    maintenanceby = models.CharField(db_column='MaintenanceBy', max_length=100)  # Field name made lowercase.
    personalname = models.CharField(db_column='PersonalName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    fk_goods = models.CharField(db_column='FK_Goods', max_length=30)  # Field name made lowercase.
    issucced = models.IntegerField(db_column='IsSucced', blank=True, null=True)  # Field name made lowercase.
    descriptions = models.CharField(db_column='Descriptions', max_length=200, blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'n_a_maintenance'


class NAStock(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    fk_goods = models.CharField(db_column='FK_Goods', max_length=30, blank=True, null=True)  # Field name made lowercase.
    totalqty = models.IntegerField(db_column='TotalQty')  # Field name made lowercase.
    isused = models.IntegerField(db_column='IsUsed')  # Field name made lowercase.
    isnew = models.IntegerField(db_column='IsNew')  # Field name made lowercase.
    isrenew = models.IntegerField(db_column='IsRenew')  # Field name made lowercase.
    isbroken = models.IntegerField(db_column='IsBroken')  # Field name made lowercase.
    fk_goods_return = models.SmallIntegerField(db_column='FK_Goods_Return', blank=True, null=True)  # Field name made lowercase.
    fk_goods_received = models.IntegerField(db_column='FK_Goods_Received', blank=True, null=True)  # Field name made lowercase.
    fk_maintenance = models.SmallIntegerField(db_column='FK_Maintenance', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'n_a_stock'


