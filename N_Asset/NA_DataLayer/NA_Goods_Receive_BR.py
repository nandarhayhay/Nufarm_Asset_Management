from django.db import models
from NA_DataLayer.common import *
from django.db.models import Count, Case, When,Value, CharField
from django.db import transaction;
from django.db import connection
from django.core import exceptions
from decimal import Decimal, DecimalException
from django.db.models import F
from django.db.models import Q
from NA_DataLayer.common import commonFunct
class NA_BR_Goods_Receive(models.Manager):
	c = None
	def PopulateQuery(self,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
		#IDapp,goods,datereceived,suplier,receivedby,pr_by,totalPurchased,totalreceived
		colKey = '';
		if columnKey == 'goods':
			colKey = 'CONCAT(g.goodsname + ' ' + g.brandname + ' ' + IFNULL(g.typeapp,' ')'
		elif columnKey == 'datereceived':
			colKey = 'ngr.datereceived'
		elif columnKey == 'suplier':
			colKey = 'sp.supliername'
		elif columnKey == 'receivedby':
			colKey ==  'emp1.receivedby'
		elif columnKey == 'pr_by':
			colKey = 'Emp2.pr_by'
		rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)
		return self.raw("SELECT ngr.IDapp,CONCAT(g.goodsname,' ', g.brandname,' ',IFNULL(g.typeapp,' ')) as goods,\
	    ngr.datereceived,sp.supliername,ngr.FK_ReceivedBy,emp1.receivedby,ngr.FK_P_R_By ,Emp2.pr_by,ngr.totalpurchased,ngr.totalreceived,ngr.CreatedDate,ngr.CreatedBy FROM n_a_goods_receive AS ngr \
	    INNER JOIN n_a_suplier AS sp ON sp.SuplierCode = ngr.FK_Suplier LEFT OUTER JOIN (SELECT IDApp,Employee_Name AS receivedby FROM employee WHERE InActive = 0 AND InActive IS NOT NULL) AS Emp1 \
		ON emp1.IDApp = ngr.FK_ReceivedBy LEFT OUTER JOIN (SELECT IDApp,Employee_Name AS pr_by FROM employee WHERE InActive = 0 AND InActive IS NOT NULL) AS Emp2 ON Emp2.IDApp = ngr.FK_P_R_By \
		INNER JOIN n_a_goods as g ON g.IDApp = ngr.FK_goods  WHERE "  + colKey + rs.Sql() + " ORDER BY ngr.IDapp DESC;")
	#idapp,fk_goods, idapp_fk_goods,datereceived, fk_suplier,supliername, totalpurchase, totalreceived, idapp_fk_received, fk_receivedby,employee_received,idapp_fk_p_r_by, fk_p_r_by,employee_pr, descriptions	
	def getData(self,IDApp):
		Query = "SELECT ngr.IDapp,ngr.FK_goods AS idapp_fk_goods,g.itemcode AS FK_goods, CONCAT(g.goodsname,' ', g.brandname,' ',IFNULL(g.typeapp,' ')) as goods,\
	    ngr.datereceived,ngr.fk_suplier,sp.supliername,ngr.fk_ReceivedBy as idapp_fK_receivedby,emp1.fk_receivedby,emp1.employee_received,ngr.FK_P_R_By AS idapp_fk_p_r_by,Emp2.fk_p_r_by,emp2.employee_pr,ngr.totalpurchased,ngr.totalreceived FROM n_a_goods_receive AS ngr \
	    INNER JOIN n_a_suplier AS sp ON sp.SuplierCode = ngr.FK_Suplier LEFT OUTER JOIN (SELECT IDApp,NIK AS fk_receivedby,employee_name AS employee_received FROM employee) AS Emp1 \
		ON emp1.IDApp = ngr.FK_ReceivedBy LEFT OUTER JOIN (SELECT IDApp,NIK AS fk_p_r_by,employee_name AS employee_pr FROM employee) AS Emp2 ON Emp2.IDApp = ngr.FK_P_R_By \
		INNER JOIN n_a_goods as g ON g.IDApp = ngr.FK_goods  WHERE ngr.IDApp = %s"
		return self.raw(Query,[IDApp])
	def hasExists(self,itemcode,datereceived,totalPurchase):
		return super(NA_BR_Goods_Receive,self).get_queryset().filter(Q(itemcode__iexact=itemcode) & Q(datereceived__icontains=datereceived)).exists()#Q(member=p1) | Q(member=p2)
	def hasReference(self,Data,mustCloseConnection):
		#cek transaksi dari mulai datereceived apakah ada pengeluaran barang untuk barang ini yang statusnya new
		if self.__class__.c is None:
			self.__class__.c = connection.cursor()
			 
		Query = "SELECT EXISTS(SELECT IDApp FROM n_a_goods_lending WHERE FK_goods = %(FK_goods)s AND IsNew = 1 AND Status = 'L' AND DateLending >= (%DateReceived)s AND Qty >= 1) \
				OR  EXISTS(SELECT IDApp FROM n_a_goods_outwards WHERE FK_Goods = %(FK_goods)s AND DateReleased >= (%DateReceived)s AND IsNew = 1 AND Qty >= 1)"
		TParams =  {'FK_goods':Data.idapp_fk_goods, 'DateReceived':Data.datereceived}
		c.execute(Query,TParams)
		hasRef = c.rowcount >0
		if mustCloseConnection:
			self.__class__.c.close()
		return hasRef
	def SaveData(self,Data,Status=StatusForm.Input):
		if self.__class__.c is None:
			 self.__class__.c = connection.cursor()
		try:
			hasRef = commonFunct.str2bool(Data.hasRefData)			
			with transaction.atomic():
				Params = {'FK_goods':Data.idapp_fk_goods, 'DateReceived':Data.datereceived, 'FK_Suplier':Data.fk_suplier, 'TotalPurchased':Data.totalpurchase,
							'TotalReceived':Data.totalreceived,'FK_ReceivedBy':Data.idapp_fk_received,'FK_P_R_By':Data.idapp_fk_p_r_by,'Descriptions':Data.Descriptions}
				if Status == StatusForm.Input:
					#insert data transaction
					Query = "INSERT INTO n_a_goods_receive (FK_goods, DateReceived, FK_Suplier, TotalPurchased, TotalReceived, FK_ReceivedBy, FK_P_R_By, CreatedDate, CreatedBy,  Descriptions) \
							VALUES (%(FK_goods)s, %(DateReceived)s, %(FK_Suplier)s, %(TotalPurchased)s, %(TotalReceived)s, %(FK_ReceivedBy)s, %(FK_P_R_By)%,(%DateReceived)s, %(CreatedBy)s,  %(Descriptions)s)"
					Params  = Params(CreatedBy=Data.CreatedBy) 
				elif Status == StatusForm.Edit:
					Query = "UPDATE n_a_goods_receive SET DateReceived = %(DateReceived)s,FK_Suplier= %(FK_Suplier)s,TotalPurchased = %(TotalPurchased)s,FK_ReceivedBy=%(FK_ReceivedBy)s,\
					FK_P_R_By = %(FK_P_R_By)%,ModifiedDate = CURRENT_DATE,ModifiedBy = %(ModifiedBy)s,Descriptions = %(Descriptions)s)"
					if not hasRef:#jika sudah ada transaksi,total received tidak bisa di edit
						Query = Query + ",TotalReceived = %(TotalReceived)s "
						Params = Params.update(Qty=Data.TotalReceived)
					Query = Query + " WHERE IDApp = %(IDApp)s"
					Params  = Params.update(ModifiedBy=Data.CreatedBy) 
					Params = Params.update(IDApp=Data.IDApp)
				self.__class__.c.execute(Query,Params)
				#update NA_stock
				Query = "SELECT EXISTS (SELECT IDApp FROM n_a_stock WHERE IDApp = %(idapp_FK_goods)s)"
				self.__class__.c.execute(Query,{'idapp_FK_goods':Data.idapp_fk_goods})
				if self.__class__.c.rowcount >0:
					if not hasRef:#jika sudah ada transaksi,stock tidak bisa di edit
						Query= "UPDATE n_a_stock SET TotalQty = TotalQty + %s,TIsNew = TIsNew + %s,TGoods_Received = TGoods_Received + %s,ModifiedDate = NOW(),ModifiedBy = %s WHERE FK_Goods = %s"
						Params = [Data.totalreceived,Data.totalreceived,Data.totalreceived,Data.CreatedBy,Data.idapp_fk_goods]
				else:
					Query = "INSERT INTO n_a_stock(FK_Goods, TotalQty, TIsUsed, TIsNew, TIsRenew, TGoods_Return, TGoods_Received, TMaintenance, CreatedDate, CreatedBy) \
							 VALUES (%(FK_goods)s,%(TotalQty)s,0,%(TIsNew),0,0,%(TotalReceived)s,0,now(),%(CreatedBy)s)"
					Params = {'FK_goods':Data.idapp_fk_goods, 'TotalQty':Data.totalreceived,'TIsNew':Data.totalreceived,'TotalReceived':Data.totalreceived, 'CreatedBy':Data.CreatedBy}
				self.__class__.c.execute(Query,Params)
		except Exception as e:
			if self.__class__.c is not None:
				self.__class__.c.close()								
			return repr(e)
		finally:
			if self.__class__.c is not None:
				self.__class__.c.close()
		return 'success'
	def delete(self,Data):
		try:
			if self.__class__.c is None:
			 self.__class__.c = connection.cursor()
			if not self.hasReference(Data,False):
				self.__class__.c.execute('Delete FROM n_a_goods_receive WHERE IDApp = %s')
				self.__class__.c.close()
				return 'success'
			else:
				self.__class__.c.close()
				raise exceptions('data has lost')	
		except Exception as e:
				if self.__class__.c is not None:
					self.__class__.c.close()
				return repr(e)
class CustomSuplierManager(models.Manager):
	def getSuplier(self,supliercode):
		return super(CustomSuplierManager,self).get_queryset().filter(supliercode__iexact=supliercode).values('supliername')
		
	def getSuplierByForm(self,searchText):
		return super(CustomSuplierManager,self).get_queryset().filter(Q(supliername__icontains=searchText) & Q(inactive__exact=0)).values('supliercode','supliername')

class custEmpManager(models.Manager):
	def getEmployee(self,nik):
		return super(custEmpManager,self).get_queryset().filter(nik__iexact=nik).values('idapp','employee_name')
	def getEmloyeebyForm(self,employeeName):
		return super(custEmpManager,self).get_queryset().filter(employee_name__icontains=employeeName).values('idapp','nik','employee_name')