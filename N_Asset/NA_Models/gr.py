from django.db import models
from NA_DataLayer.NA_Goods_Receive_BR import NA_BR_Goods_Receive
class NAGoodsReceive(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    datereceived = models.DateTimeField(db_column='DateReceived')  # Field name made lowercase.
    fk_suplier = models.CharField(db_column='FK_Suplier', max_length=30)  # Field name made lowercase.
    totalpurchased = models.SmallIntegerField(db_column='TotalPurchased')  # Field name made lowercase.
    totalreceived = models.SmallIntegerField(db_column='TotalReceived')  # Field name made lowercase.
    fk_receivedby = models.CharField(db_column='FK_ReceivedBy', max_length=50)  # Field name made lowercase.
    fk_p_r_by = models.CharField(db_column='FK_P_R_By', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate') 
    createdby = models.CharField(db_column='CreatedBy', max_length=50, blank=True, null=True) 
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True) 
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=50, blank=True, null=True)

	class Meta:
		db_table = 'n_a_goods_receive'
		app_label = ''

	objects = NA_BR_Goods_Receive()