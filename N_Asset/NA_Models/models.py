from django.db import models
from decimal import Decimal
from datetime import datetime
from NA_DataLayer.NA_Goods_BR import NA_BR_Goods
#class NABRGoods(models.Manager):
#	def serchData(columKey='',valueKey=''):
#		return super.get_queryset(NABRGoods,self).filter(columKey=valueKey)

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
	#def __str__(self):
	#	return self.nameApp