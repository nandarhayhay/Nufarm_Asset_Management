from django.db import models
from NA_DataLayer.common import *
from django.db.models import Count, Case, When,Value, CharField
from django.db import transaction;
from django.db import connection
from django.core import exceptions
from decimal import Decimal, DecimalException
from django.db.models import F
from django.db.models.functions import Concat
class NA_BR_Goods(models.Manager):
	def PopulateQuery(self,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
		NAData = None
		filterfield = columnKey + '=' 
		if criteria==CriteriaSearch.NotEqual or criteria==CriteriaSearch.NotIn:
			if criteria==CriteriaSearch.NotIn:
				filterfield = columnKey + '__in'
				
			else:
				filterfield = columnKey + '__iexact'
			NAData = super(NA_BR_Goods,self).get_queryset().exclude(**{filterfield:[ValueKey]})
			NAData.annotate(
				typeofdepreciation=Case(When(depreciationmethod__iexact='SL', then=Value('Stright Line')),
											When(depreciationmethod__iexact='DDB',then=Value('Double Declining Balance')),
											When(depreciationmethod__iexact='STYD',then=Value('Sum of The Year Digit')),
											When(depreciationmethod__iexact='SH',then=Value('Service Hours')),
											output_field=CharField())
										).values('idapp','itemcode','goodsname','brandname','typeapp','priceperunit','typeofdepreciation','unit','economiclife','placement','descriptions','inactive','createdby','createddate')	

		if criteria==CriteriaSearch.Equal:
			return super(NA_BR_Goods,self).get_queryset().filter(**{filterfield: ValueKey}).values_list('itemcode','goodsname','brandname','typeap','priceperunit','depreciationmethod','unit','economiclife','placement','descriptions','inactive')		
		elif criteria==CriteriaSearch.Greater:
			filterfield = columnKey + '__gt'
		elif criteria==CriteriaSearch.GreaterOrEqual:
			filterfield = columnKey + '__gte'
		elif criteria==CriteriaSearch.In:
			filterfield = columnKey + '__in'
		elif criteria==CriteriaSearch.Less:
			filterfield = columnKey + '__lt'
		elif criteria==CriteriaSearch.LessOrEqual:
			filterfield = columnKey + '__lte'
		elif criteria==CriteriaSearch.Like:
			filterfield = columnKey + '__icontains'
		#return super(NA_BR_Goods,self).get_queryset().filter(**{filterfield: [ValueKey] if filterfield == (columnKey + '__in') else ValueKey}).annotate(
		#			depreciation=Case(When(depreciationmethod__iexact='SL', then=Value('Stright Line')),
		#									When(depreciationmethod__iexact='DDB',then=Value('Double Declining Balance')),
		#									When(depreciationmethod__iexact='STYD',then=Value('Sum of The Year Digit')),
		#									When(depreciationmethod__iexact='SH',then=Value('Service Hours')),
		#									output_field=CharField())
		#								  ).values_list('idapp','itemcode','goodsname','brandname','typeapp','priceperunit','depreciationmethod','unit','economiclife','placement','descriptions','inactive')
		
#		from django.db.models import F

#cityList = City.objects.using(settings.DATABASE_CONF).filter(status=1).values(
#    'city_name_en', 'city_id')
## use F expression to annotate with an alias
#cityList = cityList.annotate(cityname=F('city_name_en'))
			NAData = super(NA_BR_Goods,self).get_queryset().filter(**{filterfield: [ValueKey] if filterfield == (columnKey + '__in') else ValueKey})	
		if criteria==CriteriaSearch.Beetween or criteria==CriteriaSearch.BeginWith or criteria==CriteriaSearch.EndWith:
			rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)			
			NAData = super(NA_BR_Goods,self).get_queryset().filter(S**rs.DefaultModel())
		NAData = NAData.annotate(
				typeofdepreciation=Case(When(depreciationmethod__iexact='SL', then=Value('Stright Line')),
											When(depreciationmethod__iexact='DDB',then=Value('Double Declining Balance')),
											When(depreciationmethod__iexact='STYD',then=Value('Sum of The Year Digit')),
											When(depreciationmethod__iexact='SH',then=Value('Service Hours')),
											output_field=CharField())
										).values('idapp','itemcode','goodsname','brandname','typeapp','priceperunit','typeofdepreciation','unit','economiclife','placement','descriptions','inactive','createdby','createddate')						
		return NAData
	def SearchBrand(self,term):
		return super(NA_BR_Goods,self).get_queryset().filter(brandname__istartswith=term).values('brandname').distinct()
	def SearchGoods(self,term):
		return super(NA_BR_Goods,self).get_queryset().filter(brandname__istartswith=term).values('goodsname').distinct()
	def getData(self,itemCode):
		#MyModel.objects.all().annotate(mycolumn=Value('xxx', output_field=CharField()))
		NData = super(NA_BR_Goods,self).get_queryset().filter(itemcode__exact=itemCode)
		#models.Table.objects.all().values('m', 'b').annotate(n=F('m'), a=F('b'))
		#NData = NData.annotate(typeofdepreciation=Value(depreciationmethod,output_field=CharField()),status=Value('Edit',output_field=CharField()),initializeForm=Value('',output_field=CharField()))
		NDATA = NData.annotate(status=Value('Edit',output_field=CharField()),
						 initializeForm=Value('',output_field=CharField())).values('idapp','itemcode',
											'goodsname','brandname','typeapp','priceperunit','depreciationmethod','unit',
											'economiclife','placement','descriptions','inactive','status','initializeForm')
		return NData
	def hasreferenced(self,itemcode):

		#chek existing di n_a_stock_history,
		#chek existing di n_a_stock
		#chek existing di n_a_goods_receive
		#chek existing di n_a_goods_outwards
		#chek existing di n_a_disposal
		#chek existing di n_a_acc_fa
		#chek existing di n_a_maintenance
		#chek existing di n_a_goods_return
		#	rawQuery = "SET @V_EXISTS = (SELECT EXISTS(SELECT 1 FROM #
		#existsChild = self.model.raw(
		#cursor = connection.cursor()
		#cursor.execute(rawQuery);
		hasref = False
		return hasref

	def HasExist(self,itemCode):
		return super(NA_BR_Goods,self).get_queryset().filter(itemcode__iexact=itemCode).exists()
	def setInActive(self,idapp,Inactive):
		return super(NA_BR_Goods,self).get_queryset().filter(pk=idapp).update(inactive=Inactive)
	#Model.save(force_insert=False, force_update=False, using=DEFAULT_DB_ALIAS, update_fields=None)
	def SaveData(self,Status=StatusForm.Input,**kwargs):
		obj = self.model(**kwargs);
		itemCode = obj.itemcode
		self._for_write = True
		try:
			if(Status==StatusForm.Input):
				if(self.HasExist(itemCode)):
					raise Exception('data has exists')	
				obj.save(force_insert=True, using=self.db)
				return "success"
			elif(Status==StatusForm.Edit):				
				if(not self.HasExist(itemCode)):
					raise exceptions('data has lost')		
				obj.save(force_update=True,using=self.db)
				return "success"	
		except Exception as e:					
			return repr(e)
		return obj
	def Delete(self,itemCode):
		return super(NA_BR_Goods,self).get_queryset().filter(itemcode__iexact=itemCode).delete()

class CustomManager(models.Manager):
	def getGoods(self,itemCode):
		return super(CustomManager,self).raw("SELECT IDApp,CONCAT(goodsname,' ', brandname,' ',IFNULL(typeapp,' ')) as goods FROM n_a_goods WHERE itemcode = %(itemCode)s",{'itemCode':itemCode})
	def searchGoodsByForm(self,goods_desc):#values('m', 'b').annotate(n=F('m'), a=F('b'))/renameValue=F('goods')).values('idapp,itemcode,goods')
		#get_queryset().filter(goods__icontains=goods_desc)..values('idapp,itemcode,goods')
		data = super(CustomManager,self).get_queryset().annotate(goods=F('goodsname'))
		data = data.filter(goods__icontains=goods_desc).values('idapp','itemcode','goods')
		return data