# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('NaUserUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Employee(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    nik = models.CharField(db_column='NIK', max_length=50)  # Field name made lowercase.
    employee_name = models.CharField(db_column='Employee_Name', max_length=150, blank=True, null=True)  # Field name made lowercase.
    typeapp = models.CharField(db_column='TypeApp', max_length=32, blank=True, null=True)  # Field name made lowercase.
    jobtype = models.CharField(db_column='JobType', max_length=150, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=1)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1)  # Field name made lowercase.
    telphp = models.CharField(db_column='TelpHP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    territory = models.CharField(db_column='Territory', max_length=50, blank=True, null=True)  # Field name made lowercase.
    descriptions = models.CharField(db_column='Descriptions', max_length=50, blank=True, null=True)  # Field name made lowercase.
    inactive = models.IntegerField(db_column='InActive')  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employee'


class Logevent(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    nameapp = models.CharField(db_column='NameApp', max_length=30)  # Field name made lowercase.
    typeapp = models.CharField(db_column='TypeApp', max_length=10)  # Field name made lowercase.
    descriptionsapp = models.TextField()
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'logevent'


class NAAccFa(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    fk_goods = models.IntegerField(db_column='FK_Goods')  # Field name made lowercase.
    year = models.DecimalField(db_column='Year', max_digits=10, decimal_places=2)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate')  # Field name made lowercase.
    depr_expense = models.DecimalField(db_column='Depr_Expense', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    depr_accumulation = models.DecimalField(db_column='Depr_Accumulation', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    bookvalue = models.DecimalField(db_column='BookValue', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lastupdated = models.DateTimeField(db_column='LastUpdated', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
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
        managed = False
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
        managed = False
        db_table = 'n_a_disposal'


class NAGoods(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    itemcode = models.CharField(db_column='ItemCode', max_length=30)  # Field name made lowercase.
    goodsname = models.CharField(db_column='GoodsName', max_length=150)  # Field name made lowercase.
    brandname = models.CharField(db_column='BrandName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    typeapp = models.CharField(db_column='TypeApp', max_length=32)  # Field name made lowercase.
    priceperunit = models.DecimalField(db_column='PricePerUnit', max_digits=30, decimal_places=4)  # Field name made lowercase.
    depreciationmethod = models.CharField(db_column='DepreciationMethod', max_length=3)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=30)  # Field name made lowercase.
    economiclife = models.DecimalField(db_column='EconomicLife', max_digits=10, decimal_places=2)  # Field name made lowercase.
    placement = models.CharField(db_column='Placement', max_length=50, blank=True, null=True)  # Field name made lowercase.
    descriptions = models.CharField(db_column='Descriptions', max_length=150, blank=True, null=True)  # Field name made lowercase.
    inactive = models.IntegerField(db_column='InActive', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'n_a_goods'


class NAGoodsLending(models.Model):
    idapp = models.IntegerField(db_column='IDApp')  # Field name made lowercase.
    fk_goods = models.CharField(db_column='FK_Goods', max_length=30)  # Field name made lowercase.
    isnew = models.IntegerField(db_column='IsNew')  # Field name made lowercase.
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
        managed = False
        db_table = 'n_a_goods_lending'


class NAGoodsOutwards(models.Model):
    idapp = models.IntegerField(db_column='IDApp')  # Field name made lowercase.
    fk_goods = models.CharField(db_column='FK_Goods', max_length=30)  # Field name made lowercase.
    isnew = models.IntegerField(db_column='IsNew')  # Field name made lowercase.
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
        managed = False
        db_table = 'n_a_goods_outwards'


class NAGoodsRecieve(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    fk_goods = models.IntegerField(db_column='FK_goods')  # Field name made lowercase.
    daterecieved = models.DateTimeField(db_column='DateRecieved')  # Field name made lowercase.
    fk_suplier = models.CharField(db_column='FK_Suplier', max_length=30)  # Field name made lowercase.
    totalpurchase = models.SmallIntegerField(db_column='TotalPurchase')  # Field name made lowercase.
    totalrecieved = models.SmallIntegerField(db_column='TotalRecieved')  # Field name made lowercase.
    fk_recievedby = models.CharField(db_column='FK_RecievedBy', max_length=50)  # Field name made lowercase.
    fk_p_r_by = models.CharField(db_column='FK_P_R_By', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'n_a_goods_recieve'


class NAGoodsReturn(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    fk_goods = models.CharField(db_column='FK_Goods', max_length=30)  # Field name made lowercase.
    datereturn = models.DateTimeField(db_column='DateReturn')  # Field name made lowercase.
    condition = models.CharField(db_column='Condition', max_length=1)  # Field name made lowercase.
    fk_fromemployee = models.CharField(db_column='FK_FromEmployee', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fk_usedemployee = models.CharField(db_column='FK_UsedEmployee', max_length=50, blank=True, null=True)  # Field name made lowercase.
    iscompleted = models.IntegerField(db_column='IsCompleted')  # Field name made lowercase.
    minus = models.CharField(db_column='Minus', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fk_goods_lend = models.IntegerField(db_column='FK_Goods_Lend', blank=True, null=True)  # Field name made lowercase.
    descriptions = models.CharField(db_column='Descriptions', max_length=200, blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'n_a_goods_return'


class NAMaintenance(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    requestdate = models.DateField(db_column='RequestDate', blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate')  # Field name made lowercase.
    isstillguarantee = models.TextField(db_column='IsStillGuarantee')  # Field name made lowercase.
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
        managed = False
        db_table = 'n_a_maintenance'


class NAStock(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    fk_goods = models.IntegerField(db_column='FK_Goods')  # Field name made lowercase.
    totalqty = models.IntegerField(db_column='TotalQty')  # Field name made lowercase.
    tisused = models.IntegerField(db_column='TIsUsed')  # Field name made lowercase.
    tisnew = models.IntegerField(db_column='TIsNew')  # Field name made lowercase.
    tisrenew = models.IntegerField(db_column='TIsRenew')  # Field name made lowercase.
    isbroken = models.IntegerField(db_column='IsBroken')  # Field name made lowercase.
    tgoods_return = models.SmallIntegerField(db_column='TGoods_Return', blank=True, null=True)  # Field name made lowercase.
    tgoods_recieved = models.IntegerField(db_column='TGoods_Recieved', blank=True, null=True)  # Field name made lowercase.
    tmaintenance = models.SmallIntegerField(db_column='TMaintenance', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'n_a_stock'


class NASuplier(models.Model):
    supliercode = models.CharField(db_column='SuplierCode', primary_key=True, max_length=30)  # Field name made lowercase.
    supliername = models.CharField(db_column='SuplierName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=150, blank=True, null=True)  # Field name made lowercase.
    telp = models.CharField(db_column='Telp', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hp = models.CharField(db_column='HP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contactperson = models.CharField(db_column='ContactPerson', max_length=100, blank=True, null=True)  # Field name made lowercase.
    inactive = models.CharField(db_column='InActive', max_length=3)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'n_a_suplier'


class NaUserUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    username = models.CharField(unique=True, max_length=250)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.CharField(unique=True, max_length=254)
    picture = models.CharField(max_length=100, blank=True, null=True)
    height_field = models.IntegerField(blank=True, null=True)
    width_field = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'na_user_user'


class NaUserUserGroups(models.Model):
    user = models.ForeignKey(NaUserUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'na_user_user_groups'
        unique_together = (('user', 'group'),)


class NaUserUserUserPermissions(models.Model):
    user = models.ForeignKey(NaUserUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'na_user_user_user_permissions'
        unique_together = (('user', 'permission'),)
