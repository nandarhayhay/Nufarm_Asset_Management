from django.db import models
from NA_DataLayer.common import *
from django.db.models import Count, Case, When,Value, CharField
from django.db import transaction;
from django.db import connection
from django.core import exceptions
from decimal import Decimal, DecimalException
from django.db.models import F
from NA_Models.models import NAGoodsReceive

class NA_BR_Goods_Receive:
	def PopulateQuery(self,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
		#IDapp,goods,datereceived,suplier,received_by,pr_by,totalPurchased,totalreceived
		colKey = '';
		if columnKey == 'goods':
			colKey = 'CONCAT(g.goodsname + ' ' + g.brandname + ' ' + IFNULL(g.typeapp,' ')'
		elif columnKey == 'datereceived':
			colKey = 'ngr.datereceived'
		elif columnKey == 'suplier':
			colKey = 'sp.supliername'
		elif columnKey == 'received_by':
			colKey ==  'emp1.received_by'
		elif columnKey == 'pr_by':
			colKey = 'Emp2.pr_by'
		rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)
		return NAGoodsReceive._default_manager.raw("SELECT ngr.IDapp,CONCAT(g.goodsname + ' ' + g.brandname + ' ' + IFNULL(g.typeapp,' ') as goods , \
	    ngr.datereceived,sp.supliername,ngr.FK_ReceivedBy,emp1.received_by,FK_P_R_By ,Emp2.pr_by,ngr.totalpurchase,ngr.totalreceived FROM n_a_goods_receive AS ngr \
		INNER JOIN n_a_suplier AS sp ON sp.SuplierCode = ngr.FK_Suplier LEFT OUTER JOIN (SELECT IDApp,Employee_Name AS Received_By FROM employee \
		WHERE InActive = 0 AND InActive IS NOT NULL) AS Emp1 ON emp1.IDApp = ngr.FK_ReceivedBy LEFT OUTER JOIN (SELECT IDApp,Employee_Name AS pr_by FROM employee \
	    WHERE InActive = 0 AND InActive IS NOT NULL) AS Emp2 ON Emp2.IDApp = ngr.FK_P_R_By INNER JOIN n_a_goods g ON g.IDApp = ngr.FK_goods  WHERE "  + colKey + rs.Sql() + " ORDER BY ngr.IDapp DESC")