from django.db import models
from NA_DataLayer.common import *
from django.db.models import Count, Case, When,Value, CharField
from django.db import transaction;
from django.db import connection
from django.core import exceptions
from decimal import Decimal, DecimalException
from django.db.models import F
from django.db.models import Q
from decimal import Decimal
from NA_DataLayer.common import commonFunct
class NA_BR_Goods_Receive(models.Manager):
	c = None
	def PopulateQuery(self,orderFields,sortIndice,pageSize,PageIndex,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
		#IDapp,goods,datereceived,suplier,receivedby,pr_by,totalPurchase,totalreceived
		colKey = '';
		if columnKey == "goods":
			colKey = """CONCAT(g.goodsname, ' ', g.brandname, ' ', IFNULL(g.typeapp,' '))"""
		elif columnKey == 'datereceived':
			colKey = "ngr.datereceived"
		elif columnKey == "supliername":
			colKey = "sp.supliername"
		elif columnKey == 'receivedby':
			colKey =  "emp1.receivedby"
		elif columnKey == 'pr_by':
			colKey = "Emp2.pr_by"
		elif columnKey == "RefNO":
			colKey = "ngr.refno"
		elif columnKey == 'createdby':
			colKey = "ngr.createdby"
		rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)
		self.__class__.c = connection.cursor()
		cur = self.__class__.c
		Query = "DROP TEMPORARY TABLE IF EXISTS T_Receive_Manager"
		cur.execute(Query)		
		#CREATE TEMPORARY TABLE IF NOT EXISTS  temp_table ( INDEX(col_2) ) ENGINE=MyISAM AS (SELECT col_1, coll_2, coll_3  FROM mytable)
		Query = """CREATE TEMPORARY TABLE T_Receive_Manager ENGINE=MyISAM AS (SELECT ngr.IDApp,ngr.refno,g.goodsname as goods,\
	    ngr.datereceived,sp.supliername,ngr.FK_ReceivedBy,emp1.receivedby,ngr.FK_P_R_By ,Emp2.pr_by,ngr.totalpurchase,ngr.totalreceived,CONCAT(IFNULL(ngr.descriptions,' '),', ITEMS : ', IFNULL(ngr.DescBySystem,' ')) AS descriptions, ngr.CreatedDate,ngr.CreatedBy FROM n_a_goods_receive AS ngr \
	    INNER JOIN n_a_suplier AS sp ON sp.SuplierCode = ngr.FK_Suplier LEFT OUTER JOIN (SELECT IDApp,Employee_Name AS receivedby FROM employee WHERE InActive = 0 AND InActive IS NOT NULL) AS Emp1 \
		ON emp1.IDApp = ngr.FK_ReceivedBy LEFT OUTER JOIN (SELECT IDApp,Employee_Name AS pr_by FROM employee WHERE InActive = 0 AND InActive IS NOT NULL) AS Emp2 ON Emp2.IDApp = ngr.FK_P_R_By \
		INNER JOIN n_a_goods as g ON g.IDApp = ngr.FK_goods  WHERE """  + colKey + rs.Sql() + ")"
		cur.execute(Query)	
		strLimit = '300'
		if int(PageIndex) <= 1:
			strLimit = '0'
		else:
			strLimit = str(int(PageIndex)*int(pageSize))
		if orderFields != '':
			#Query = """SELECT * FROM T_Receive_Manager """ + (("ORDER BY " + ",".join(orderFields)) if len(orderFields) > 1 else " ORDER BY " + orderFields[0]) + (" DESC" if sortIndice == "" else sortIndice) + " LIMIT " + str(pageSize*(0 if PageIndex <= 1 else PageIndex)) + "," + str(pageSize)
			Query = """SELECT * FROM T_Receive_Manager ORDER BY """ + orderFields + (" DESC" if sortIndice == "" else ' ' + sortIndice) + " LIMIT " + strLimit + "," + str(pageSize)
		else:			
			Query = """SELECT * FROM T_Receive_Manager ORDER BY IDApp LIMIT """ + strLimit + "," + str(pageSize)
		cur.execute(Query)
		result = query.dictfetchall(cur)
		#get countRows
		Query = """SELECT COUNT(*) FROM T_Receive_Manager"""
		cur.execute(Query)
		row = cur.fetchone()
		totalRecords = row
		cur.close()
		return (result,totalRecords)
	#idapp,fk_goods, idapp_fk_goods,datereceived, fk_suplier,supliername, totalpurchase, totalreceived, idapp_fk_received, fk_receivedby,employee_received,idapp_fk_p_r_by, fk_p_r_by,employee_pr, descriptions	
	def getRefNO(self,searchRefNO):
		return super(NA_BR_Goods_Receive,self).get_queryset().filter(refno__istartswith=searchRefNO).values('refno').distinct()
	def getData(self,IDApp):
		self.__class__.c = connection.cursor()
		cur = self.__class__.c
		Query = """SELECT ngr.idapp,ngr.refno,ngr.FK_goods AS idapp_fk_goods,g.itemcode AS fk_goods, goodsname as goods_desc,g.economiclife, \
	    ngr.datereceived,ngr.fk_suplier,sp.supliername,ngr.fk_ReceivedBy as idapp_fk_receivedby,emp1.fk_receivedby,emp1.employee_received,ngr.FK_P_R_By AS idapp_fk_p_r_by,Emp2.fk_p_r_by,emp2.employee_pr,ngr.totalpurchase,ngr.totalreceived,ngr.descriptions,ngr.descbysystem FROM n_a_goods_receive AS ngr \
	    INNER JOIN n_a_suplier AS sp ON sp.SuplierCode = ngr.FK_Suplier LEFT OUTER JOIN (SELECT IDApp,NIK AS fk_receivedby,employee_name AS employee_received FROM employee) AS Emp1 \
		ON emp1.IDApp = ngr.FK_ReceivedBy LEFT OUTER JOIN (SELECT IDApp,NIK AS fk_p_r_by,employee_name AS employee_pr FROM employee) AS Emp2 ON Emp2.IDApp = ngr.FK_P_R_By \
		INNER JOIN n_a_goods as g ON g.IDApp = ngr.FK_goods  WHERE ngr.IDApp = %s"""
		cur.execute(Query,[IDApp])
		data = query.dictfetchall(cur)
		cur.close()
		return data
	def getDetailData(self,fkApp,idapp_fk_goods):
		#GET idapp_fk_goods
		self.__class__.c = connection.cursor()
		cur = self.__class__.c
		Query = """SELECT grd.*, CONVERT((EXISTS(SELECT serialnumber FROM n_a_goods_outwards WHERE FK_goods = %(FK_Goods)s AND SerialNumber = grd.SerialNumber)  \
												OR EXISTS(SELECT serialnumber FROM n_a_goods_lending WHERE FK_goods = %(FK_Goods)s AND SerialNumber = grd.SerialNumber) \
												OR EXISTS(SELECT serialnumber FROM n_a_goods_return WHERE FK_goods = %(FK_Goods)s AND SerialNumber = grd.SerialNumber) \
											    OR EXISTS(SELECT serialnumber FROM n_a_maintenance WHERE FK_goods = %(FK_Goods)s AND SerialNumber = grd.SerialNumber)),INT)  AS HasRef \
				FROM n_a_goods_receive_detail AS grd WHERE grd.FK_App = %(FKApp)s ORDER By grd.IDApp ASC """
		cur.execute(Query,{'FKApp':fkApp,'FK_Goods':idapp_fk_goods})
		data = query.dictfetchall(cur)
		cur.close()
		return data
	def hasEsitsSN(self,SN):
		self.__class__.c = connection.cursor()
		cur = self.__class__.c
		Query = """SELECT EXISTS(SELECT SerialNumber FROM n_a_goods_receive_detail WHERE serialnumber = %s)"""
		cur.execute(Query,[SN])
		row = cur.fetchone()
		cur.close()
		return int(row[0]) > 0

	def hasExists(self,idapp_fk_goods,datereceived,totalPurchase):
		#An error occurred: FieldError('Related Field got invalid lookup: iexact',)
		return super(NA_BR_Goods_Receive,self).get_queryset().filter(Q(idapp_fk_goods=idapp_fk_goods) & Q(datereceived=datereceived) & Q(totalpurchase=totalPurchase)).exists()#Q(member=p1) | Q(member=p2)
	def hasReference(self,Data,Ccur):
		#cek transaksi dari mulai datereceived apakah ada pengeluaran barang untuk barang ini yang statusnya new
		cur = None	
		if Ccur is None:
			cur = connection.cursor()
		else :
			cur = Ccur
		Query ="""SELECT DISTINCT(SerialNumber) AS SerialNumber FROM n_a_goods_receive_detail WHERE FK_App = %s AND SerialNumber IS NOT NULL"""
		cur.execute(Query,[Data['idapp']])
		hasRef = False
		results = [item	for item in cur.fetchall()]		
		if len(results) > 0:
			strResult = ''
			for i in range(len(results)):
				strResult += results[i][0]
				if i < len(results)-1:
					strResult += ','				
			#strResult = ','.join(results[i][0]*len(results))
			Query = """SELECT EXISTS(SELECT IDApp FROM n_a_goods_lending WHERE FK_goods = %s AND  DateLending >= %s  AND SerialNumber  IN ('{0}')) \
					OR  EXISTS(SELECT IDApp FROM n_a_goods_outwards WHERE FK_Goods = %s AND DateReleased >= %s AND IsNew = 1  AND SerialNumber  IN ('{1}') )""".format(strResult,strResult)
			TParams =  [Data['idapp_fk_goods'], Data['datereceived'],Data['idapp_fk_goods'], Data['datereceived']]
			cur.execute(Query,TParams)
			row = cur.fetchone()
			hasRef = commonFunct.str2bool(str(row[0]))		
		return hasRef
	def hasRefDetail(self,data):
		self.__class__.c = connection.cursor()
		cur = self.__class__.c
		Query = """SELECT EXISTS(SELECT IDApp FROM n_a_goods_lending WHERE FK_goods = %s AND IsNew = 1  AND DateLending >= %s AND SerialNumber = %s) \
					OR  EXISTS(SELECT IDApp FROM n_a_goods_outwards WHERE FK_Goods = %s AND DateReleased >= %s AND IsNew = 1 AND SerialNumber = %s)"""
		TParams =  [data['idapp_fk_goods'], data['datereceived'],data['serialnumber'],data['idapp_fk_goods'], data['datereceived'],data['serialnumber']]
		cur.execute(Query,TParams)
		row = cur.fetchone()
		hasRef = commonFunct.str2bool(str(row[0]))	
		#if not hasRef:
		#	Query = """SELECT EXISTS(SELECT IDApp FROM n_a_goods_lending WHERE FK_goods = %s AND IsNew = 1  AND DateLending >= %s  AND TypeApp = %s) \
		#			OR  EXISTS(SELECT IDApp FROM n_a_goods_outwards WHERE FK_Goods = %s AND DateReleased >= %s AND Qty >= 1 AND TypeApp = %s)"""
		#	TParams =  [data['idapp_fk_goods'], data['datereceived'],data['typeapp'],data['idapp_fk_goods'], data['datereceived'],data['typeapp']]
		#	cur.execute(Query,TParams)
		#	hasRef = cur.rowcount >0
		cur.close()
		return hasRef
	def SaveData(self,Data,Status=StatusForm.Input):
		self.__class__.c = connection.cursor()
		cur = self.__class__.c
		try:
			hasRef = commonFunct.str2bool(str(Data['hasRefData']))		
			(totalNew,totalReceived,totalUsed,totalReturn,totalRenew,totalMaintenance,TotalSpare) = commonFunct.getTotalGoods(int(Data['idapp_fk_goods']),cur,Data['createdby'])#return(totalUsed,totalReceived,totalReturn,totalRenew,totalMaintenance,TotalSpare)		
			if Status == StatusForm.Input:
				totalNew = totalNew + int(Data['totalreceived'])
				totalReceived = totalReceived + int(Data['totalreceived'])
			with transaction.atomic():
				#sum kan total Receive
				#Query = """SELECT SUM(T
				Params = {'RefNO':Data['refno'],'FK_goods':Data['idapp_fk_goods'], 'DateReceived':Data['datereceived'], 'FK_Suplier':Data['fk_suplier'], 'TotalPurchase':Data['totalpurchase'],
							'TotalReceived':Data['totalreceived'],'FK_ReceivedBy':Data['idapp_fk_receivedby'],'FK_P_R_By':Data['idapp_fk_p_r_by'],'Descriptions':Data['descriptions'],'descbysystem':Data['descbysystem']}
				dataDetail = list(Data.get('dataForGridDetail'));
				detCount = len(dataDetail)
					#dataDetail = object_list
				if Status == StatusForm.Input:
					#insert data transaction
					Query = """INSERT INTO n_a_goods_receive (REFNO,FK_goods, DateReceived, FK_Suplier, TotalPurchase, TotalReceived, FK_ReceivedBy, FK_P_R_By, CreatedDate, CreatedBy,  Descriptions,descbysystem) \
							VALUES (%(RefNO)s,%(FK_goods)s, %(DateReceived)s, %(FK_Suplier)s, %(TotalPurchase)s, %(TotalReceived)s, %(FK_ReceivedBy)s, %(FK_P_R_By)s,CURRENT_DATE, %(CreatedBy)s,  %(Descriptions)s,%(descbysystem)s)"""
					Params.update(CreatedBy=Data['createdby']) 
					cur.execute(Query,Params)
					#get primary key
					cur.execute('SELECT last_insert_id()')
					row = cur.fetchone()
					FKApp = row[0]
					#Insert Detail
					
					if detCount > 0:
						#tambahkan detail pada FK_App
						details = []
						detail = []
						for i in range(detCount):
							dataDetail[i]['fkapp'] = FKApp
							details.append(tuple(dataDetail[i].values()))
						#details = [list(d.values()) for d in dataDetail]#hasilnya harus seperti listTuple [('RefNO', 'RefNO', 'varchar'), ('Goods Descriptions', 'goods', 'varchar'), ('Date Received', 'datereceived', 'datetime'), ('Suplier Name', 'suplier', 'varchar'), ('Received By', 'receivedby', 'varchar'), ('PR By', 'pr_by', 'varchar'), ('Total Purchased', 'totalpurchase', 'int'), ('Total Received', 'totalreceived', 'int')]	
						#'fkapp', 'BrandName', 'Price/Unit', 'Type', 'Serial Number', 'warranty', 'End of Warranty', 'CreatedBy', 
						Query = """INSERT INTO n_a_goods_receive_detail (FK_App, BrandName, PricePerUnit, TypeApp, SerialNumber, warranty, EndOfWarranty, CreatedDate, CreatedBy)\
									VALUES(%s,%s, %s, %s, %s, %s, %s, CURRENT_DATE, %s)"""
						cur.executemany(Query,details)
				elif Status == StatusForm.Edit:
					hasChangedHeader = commonFunct.str2bool(str(Data['hasChangedHeader']))
					hasChangedDetail = commonFunct.str2bool(str(Data['hasChangedDetail']))				
					#totalpurchase dan totalreceived bisa di edit bila hasref = 0
					if hasChangedHeader:
						Query = """UPDATE n_a_goods_receive SET RefNO = %(RefNO)s,DateReceived =  %(DateReceived)s,FK_Suplier = %(FK_Suplier)s,TotalPurchase = %(TotalPurchase)s, FK_ReceivedBy = %(FK_ReceivedBy)s,\
									FK_P_R_By = %(FK_P_R_By)s,ModifiedDate = CURRENT_DATE,ModifiedBy = %(ModifiedBy)s,Descriptions = %(Descriptions)s """
						if not hasRef:#jika sudah ada transaksi,total received tidak bisa di edit
							Query = Query + """,TotalReceived = %(TotalReceived)s,DescBySystem = %(descbysystem)s """
							Params.update(Qty=Data['totalreceived'])
						Query = Query + """ WHERE IDApp = %(IDApp)s"""
						Params.update(ModifiedBy=Data['createdby']) 
						Params.update(IDApp=Data['idapp'])
						cur.execute(Query,Params)
					if hasChangedDetail:
						if detCount > 0:
							for i in range(detCount):
							#check apakah data sudah ada untuk memastikan, jika memang ada update data,terlebih dulu check reference data
								Query = "SELECT EXISTS(SELECT IDApp FROM n_a_goods_receive_detail WHERE IDApp = %(IDApp)s) "
								cur.execute(Query,{'IDApp':dataDetail[i]['idapp']})
								row = cur.fetchone()
								HasRows = commonFunct.str2bool(str(row[0]))
								if HasRows:
									#data sudah ada
									#check hasrefDetail jika data sudah ada reference data anak
									hasRefDetail = commonFunct.str2bool(str(dataDetail[i]['HasRef']))
									if not hasRefDetail:
										ParDetails = {'idapp_fk_goods':Data['idapp_fk_goods'],'datereceived':Data['datereceived'],'serialnumber':dataDetail[i]['serialnumber']}
										hasRefDetail = self.hasRefDetail(ParDetails)
									if not hasRefDetail:
										Query = """UPDATE n_a_goods_receive_detail SET BrandName=%(BrandName)s,PricePerUnit=%(PricePerUnit)s,TypeApp=%(TypeApp)s,SerialNumber=%(SerialNumber)s,\
													warranty=%(warranty)s,EndOfWarranty=%(EndOfWarranty)s,ModifiedBy=%(ModifiedBy)s,ModifiedDate=CURRENT_DATE WHERE IDApp = %(IDApp)s """			
										cur.execute(Query,{'BrandName':dataDetail[i]['brandname'],'PricePerUnit':dataDetail[i]['priceperunit'],'TypeApp':dataDetail[i]['typeapp'],\
														'SerialNumber':dataDetail[i]['serialnumber'],'warranty':dataDetail[i]['warranty'],'EndOfWarranty':dataDetail[i]['endofwarranty'],'ModifiedBy':dataDetail[i]['modifiedby'],'IDApp':dataDetail[i]['idapp']})
								else:
									Query = """INSERT INTO n_a_goods_receive_detail (FK_App, BrandName, PricePerUnit, TypeApp, SerialNumber, warranty, EndOfWarranty, CreatedDate, CreatedBy) \
											VALUES(%s,%s, %s, %s, %s, %s, %s, CURRENT_DATE, %s) """
									cur.execute(Query,[Data['idapp'],dataDetail[i]['brandname'],dataDetail[i]['priceperunit'],dataDetail[i]['typeapp'],dataDetail[i]['serialnumber'],dataDetail[i]['warranty'],dataDetail[i]['endofwarranty'],dataDetail[i]['modifiedby']])	
				#update NA_stock
				Query = """SELECT EXISTS (SELECT IDApp FROM n_a_stock WHERE FK_goods = %(idapp_FK_goods)s)"""
				cur.execute(Query,{'idapp_FK_goods':Data['idapp_fk_goods']})
				row = cur.fetchone()
				HasRows = commonFunct.str2bool(str(row[0]))
				
				if HasRows:
					(totalNew,totalReceived,totalUsed,totalReturn,totalRenew,totalMaintenance,TotalSpare) = commonFunct.getTotalGoods(int(Data['idapp_fk_goods']),cur,Data['createdby'])#return(totalUsed,totalReceived,totalReturn,totalRenew,totalMaintenance,TotalSpare)		
					Query= """UPDATE n_a_stock SET TIsNew =  %s,TGoods_Received = %s,ModifiedDate = NOW(),ModifiedBy = %s WHERE FK_Goods = %s"""
					Params = [totalNew,totalReceived,Data['createdby'],Data['idapp_fk_goods']]
					cur.execute(Query,Params)
					cur.close()	
					return 'success'
				else:
					Query = """INSERT INTO n_a_stock (FK_Goods, T_Goods_Spare, TIsUsed, TIsNew, TIsRenew, TGoods_Return, TGoods_Received, TMaintenance, CreatedDate, CreatedBy) \
							 VALUES (%(FK_goods)s,%(T_Goods_Spare)s,0,%(TIsNew)s,0,0,%(TotalReceived)s,0,NOW(),%(CreatedBy)s)"""
					Params = {'FK_goods':Data['idapp_fk_goods'], 'T_Goods_Spare':TotalSpare,'TIsNew':totalNew,'TotalReceived':totalReceived, 'CreatedBy':Data['createdby']}
				cur.execute(Query,Params)
				cur.close()
		except Exception as e:
			cur.close()								
			return repr(e)	
		return 'success'
	def deleteDetail(self,Data):
		self.__class__.c = connection.cursor()
		cur = self.__class__.c
		#cek reference detail
		#[data.idapp_fk_goods, data.datereceived,data.serialnumber,data.idapp_fk_goods, data.datereceived,data.serialnumber]
		Query = """SELECT ngr.IDApp AS idapp_fk_goods,ngr.datereceived,ngd.typeapp,ngd.serialnumber FROM n_a_goods_receive ngr INNER JOIN n_a_goods_receive_detail ngd \
					ON ngd.FK_App = ngr.IDApp WHERE ngd.idapp = %s"""
		cur.execute(Query,[Data['idapp']])
		if cur.rowcount > 0:
			row = cur.fetchone()
			Params = {'idapp_fk_goods':row[0], 'datereceived':row[1],'typeapp':row[2],'serialnumber':row[3]}
			if self.hasRefDetail(Params):
				cur.close()
				return 'Can not delete data\Data has child-referenced'
			try:
				with transaction.atomic():
					FKApp = int(row[0])					
					(totalNew,totalReceived,totalUsed,totalReturn,totalRenew,totalMaintenance,TotalSpare) = commonFunct.getTotalGoods(FKApp,cur,Data['deletedby'])#return(totalUsed,totalReceived,totalReturn,totalRenew,totalMaintenance,TotalSpare)
					Query = """DELETE FROM n_a_goods_receive_detail WHERE IDApp = %s"""
					cur.execute(Query,[Data['idapp']]);
					#update stock
					Query = """SELECT COUNT(IDApp) FROM n_a_goods_receive_detail WHERE FK_App = %s"""
					cur.execute(Query,[FKApp])
					row = cur.fetchone()
					tgoodsRec = int(row[0])
					Query = """UPDATE n_a_goods_receive SET TotalReceived = %s, ModifiedBy = %s, ModifiedDate = NOW() WHERE IDApp = %s"""
					cur.execute(Query,[tgoodsRec,Data['deletedby'],FKApp])
					totalNew = totalNew - 1
					totalReceived = totalReceived - 1

					Query= """UPDATE n_a_stock SET TIsNew =  %s,TGoods_Received = %s,ModifiedDate = NOW(),ModifiedBy = %s WHERE FK_Goods = %s"""
					Params = [totalNew,totalReceived,Data['deletedby'],FKApp]
					cur.execute(Query,Params)

					cur.close()	
					return 'success'
			except Exception as e :
				cur.close()
				return repr(e)
		cur.close()						
		return 'success'	
	def delete(self,Data):
		try:
			self.__class__.c = connection.cursor()
			cur = self.__class__.c
			(totalNew,totalReceived,totalUsed,totalReturn,totalRenew,totalMaintenance,TotalSpare) = commonFunct.getTotalGoods(int(Data['idapp_fk_goods']),cur,Data['deletedby'])#return(totalUsed,totalReceived,totalReturn,totalRenew,totalMaintenance,TotalSpare)
			row = {};treceived = 0
			cur.execute("""SELECT COUNT(IDApp) FROM n_a_goods_receive_detail WHERE FK_App = %s""",[Data['idapp']])
			if cur.rowcount >0:
				row = cur.fetchone()
				treceived = int(row[0])
			with transaction.atomic():
				if not self.hasReference(Data,cur):		
					cur.execute("""Delete FROM n_a_goods_receive_detail WHERE FK_App = %s""",[Data['idapp']])
					cur.execute("""Delete FROM n_a_goods_receive WHERE IDApp = %s""",[Data['idapp']])
					#update stock
					totalNew = totalNew - treceived
					totalReceived = totalReceived - treceived
					Query= """UPDATE n_a_stock SET TIsNew =  %s,TGoods_Received = %s,ModifiedDate = NOW(),ModifiedBy = %s WHERE FK_Goods = %s"""
					Params = [totalNew,totalReceived,Data['deletedby'],[Data['idapp']]]
					cur.execute(Query,Params)
					cur.close()	
					return 'success'
				else:
					cur.close()
					return 'Can not delete data\Data has child-referenced'
		except Exception as e:
			cur.close()
			return repr(e)
	def getBrandsForDetail(self,FKGoods,searchText):

		#ambil data di receive_goods_detail,union dengan brandname di table goods
		if FKGoods is not None:
			Query =  """SELECT DISTINCT(ngd.BrandName) FROM n_a_goods_receive_detail ngd INNER JOIN n_a_goods_receive ngr ON ngr.IDApp = ngd.FK_App WHERE ngd.BrandName LIKE '%{0!s}%' AND ngr.FK_Goods = {1!s}"""
			Query = Query.format(searchText,FKGoods)
		else:
			Query = "SELECT DISTINCT(BrandName) FROM n_a_goods WHERE BrandName LIKE '%{0!s}%' \
				   UNION \
				   SELECT DISTINCT(BrandName) FROM n_a_goods_receive_detail WHERE BrandName LIKE '%{1!s}%' """
		self.__class__.c = connection.cursor()
		cur = self.__class__.c
		if FKGoods is not None:
			cur.execute(Query)
		else:
			cur.execute(Query.format(searchText,searchText))
		data = query.dictfetchall(cur)
		cur.close()
		return data
	def getTypesApp(self,FKGoods,searchText):
		Query = """SELECT DISTINCT(ngd.TypeApp) FROM n_a_goods_receive_detail ngd INNER JOIN n_a_goods_receive ngr ON ngr.IDApp = ngd.FK_App WHERE ngd.TypeApp LIKE '%{0!s}%' AND ngr.FK_Goods = {1!s}"""
		Query = Query.format(searchText,FKGoods)
		self.__class__.c = connection.cursor()
		cur = self.__class__.c
		cur.execute(Query)
		data = query.dictfetchall(cur)
		cur.close()
		return data
class CustomSuplierManager(models.Manager):
	def getSuplier(self,supliercode):
		return super(CustomSuplierManager,self).get_queryset().filter(supliercode__iexact=supliercode).values('supliername')
		
	def getSuplierByForm(self,searchText):
		return super(CustomSuplierManager,self).get_queryset().filter(Q(supliername__icontains=searchText) & Q(inactive__exact=0)).values('supliercode','supliername')

class custEmpManager(models.Manager):
	def getEmployee(self,nik):
		return super(custEmpManager,self).get_queryset().filter(nik__iexact=nik).values('idapp','employee_name')
	def getEmloyeebyForm(self,employeeName):
		return super(custEmpManager,self).get_queryset().filter(Q(employee_name__icontains=employeeName) & Q(inactive__exact=0)).values('idapp','nik','employee_name')