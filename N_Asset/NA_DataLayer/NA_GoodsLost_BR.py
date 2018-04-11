from django.db import models, connection
from NA_DataLayer.common import  query, ResolveCriteria, StatusForm, CriteriaSearch, DataType
from django.db.models import F, Value, Case, When, CharField
from django.db.models.functions import Concat
class NA_BR_GoodsLost(models.Manager):
    def PopulateQuery(self,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar,sidx='idapp',sord='desc'):
        filterfield = columnKey
        if criteria==CriteriaSearch.NotEqual or criteria==CriteriaSearch.NotIn:
            if criteria==CriteriaSearch.NotIn:
                filterfield = columnKey + '__in'
            else:
                filterfield = columnKey + '__iexact'
        elif criteria==CriteriaSearch.Equal:
            filterfield = columnKey + '__exact'
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

        qs = super(NA_BR_GoodsLost,self).get_queryset().annotate(goods=Concat(F('fk_goods__goodsname'), Value(' '), \
                                                                            F('fk_goods__brandname'), Value(' '), F('fk_goods__typeapp')),
                                                                 itemcode=F('fk_goods__itemcode'),
                                                                 lost_by=Case(When(fk_lostby=None,then=Value(' ')),
                                                                              When(fk_lostby=int,then=F('fk_lostby__employee_name')),
                                                                              output_field=CharField()))
        #_getGoods_lending = qs.select_related('fk_goods_lending').annotate(used_by=F('fk_goods_lending__fk_employee__employee_name'),
        #                                                               resp_person=F('fk_goods_lending__fk_responsibleperson__employee_name')).values(
        #                                                                   'idapp','goods','itemcode','serialnumber','fk_fromgoods','used_by','lost_by',
        #                                                                   'resp_person','descriptions','createddate','createdby')
        #_getGoods_outwards = qs.select_related('fk_goods_outwards').annotate(used_by=F('fk_goods_outwards__fk_employee__employee_name'),
        #                                                               resp_person=F('fk_goods_outwards__fk_responsibleperson__employee_name')).values(
        #                                                                   'idapp','goods','itemcode','serialnumber','fk_fromgoods','used_by','lost_by','resp_person',
        #                                                                   'descriptions','createddate','createdby')
        #_getMaintenance = qs.select_related('fk_maintenance').annotate(used_by=F('fk_goods_maintenance__fk_employee__employee_name'),
        #                                                               resp_person=F('fk_goods_outwards__fk_responsibleperson__employee_name')).values(
        #                                                                   'idapp','goods','itemcode','serialnumber','fk_fromgoods','used_by','lost_by','resp_person',
        #                                                                   'descriptions','createddate','createdby')
        #goods_data = _getGoods_lending.union(_getGoods_outwards)
        #cur = connection.cursor()
        #cur.execute("DROP TEMPORARY TABLE IF EXISTS T_GoodsLost_Manager")
        #rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)
        #Query = """CREATE TEMPORARY TABLE T_GoodsLost_Manager ENGINE=InnoDB AS(SELECT gls.idapp, gls.fk_goods, gls.fk_fromgoods, gls.serialnumber,ngo.fk_employee AS used_by,ngo.fk_responsibleperson AS resp_person,gls.fk_lostby AS lost_by,
        #gls.datelost, gls.reason, gls.descriptions, gls.createddate, gls.createdby, CONCAT(g.goodsname, ' ',g.brandname, ' ',gls.typeapp) as goods, g.itemcode FROM
        #n_a_goods_lost gls INNER JOIN n_a_goods g ON gls.fk_goods = g.idapp INNER JOIN  n_a_goods_outwards ngo ON gls.fk_goods_outwards=ngo.idapp AND gls.fk_goods_outwards IS NOT NULL WHERE """
        #Query = Query + columnKey + rs.Sql() + " ORDER BY " + sidx + " " + sord + ")"
        #cur.execute(Query)
        #cur.execute("SELECT * FROM T_GoodsLost_Manager")
        #result = query.dictfetchall(cur)
        #cur.close()
        return qs.values('idapp','goods','itemcode','serialnumber','fk_fromgoods','lost_by','descriptions','createddate','createdby')

    def SaveData(self, statusForm=StatusForm.Input, **data):
        cur = connection.cursor()
        Params = {'FK_Goods':data['fk_goods'],'FK_FromGoods':data['fk_fromgoods'],'SerialNumber':data['serialNumber'],'TypeApp':data['typeApp'],
                  'FK_Goods_Outwards':data['fk_goods_outwards'],'FK_LostBy':data['fk_lostby'],'FK_Goods_Lending':data['fk_goods_lending'],
                  'FK_Maintenance':data['fk_maintenance'],'Reason':data['reason'],'Descriptions':data['descriptions']}
        if statusForm == StatusForm.Input:
            if self.dataExist(serialnumber=data['serialNumber'],status='L'):
                return ('HasExist',)
            else:
                Params['CreatedDate'] = data['createddate']
                Params['CreatedBy'] = data['createdby']
                Query = """INSERT INTO n_a_goods_lost(fk_goods, fk_fromgoods, serialnumber, typeapp, fk_goods_outwards,fk_goods_lending,fk_maintenance,fk_lostby,reason,descriptions,
                createddate, createdby) VALUES(%(FK_Goods)s, %(FK_FromGoods)s, %(SerialNumber)s, %(TypeApp)s, %(FK_Goods_Outwards)s, %(FK_Goods_Lending)s, %(FK_Maintenance)s, %(FK_LostBy)s,
                %(Reason)s,%(Descriptions)s, %(CreatedDate)s, %(CreatedBy)s)"""
        elif statusForm == StatusForm.Edit:
            Params['IDApp'] = data['idapp']
            Params['ModifiedDate'] = data['modifieddate']
            Params['ModifiedBy'] = data['modifiedby']
            Params['Status'] = data['status_goods']
            Query = """UPDATE n_a_goods_lost SET fk_goods=%(FK_Goods)s, fk_fromgoods=%(FK_FromGoods)s, serialnumber=%(SerialNumber)s,typeapp=%(TypeApp)s,
            fk_goods_outwards=%(FK_Goods_Outwards)s, fk_goods_lending=%(FK_Goods_Lending)s, fk_maintenance=%(FK_Maintenance)s,fk_lostby=%(FK_LostBy)s,
            status=%(Status)s,descriptions=%(Descriptions)s, modifieddate=%(ModifiedDate)s,modifiedby=%(ModifiedBy)s
            WHERE idapp = %(IDApp)s"""
        cur.execute(Query,Params)
        row = cur.lastrowid
        connection.close()
        return ('success',row)

    #Rimba pinjam laptop dell KN7841, sudah dikembalikan


    """DROP TEMPORARY TABLE IF EXISTS T_GoodsLost_Manager;
CREATE TEMPORARY TABLE T_GoodsLost_Manager ENGINE=InnoDB AS (SELECT gls.idapp, gls.fk_goods, gls.fk_fromgoods, gls.serialnumber,gls.fk_goods_outwards,gls.fk_goods_lending,empl1.fk_employee,
        gls.datelost, gls.reason, gls.descriptions, gls.createddate, gls.createdby, CONCAT(g.goodsname, ' ',g.brandname, ' ',gls.typeapp) as goods, g.itemcode FROM
        n_a_goods_lost gls INNER JOIN n_a_goods g ON gls.fk_goods = g.idapp INNER JOIN n_a_goods_lending ngl ON gls.FK_Goods_Lending = ngl.idapp LEFT OUTER JOIN (SELECT idapp,employee_name AS fk_employee FROM employee) AS empl1 ON ngl.FK_Employee=empl1.idapp);
SELECT * FROM T_GoodsLost_Manager;"""


    #Query_old = """CREATE TEMPORARY TABLE T_goods_byForm ENGINE=InnoDB AS (SELECT * FROM (SELECT ngo.idapp, g.itemcode,@table_name := 'GO' AS tbl_name,
    #    CONCAT(g.goodsname, ' ',g.brandname, ' ',grd.typeapp) as goods,grd.serialnumber,empl1.idapp as used_idapp, empl2.fk_responsibleperson,empl1.used_by,
    #    empl2.empl_resp, empl1.used_nik, empl2.resp_nik FROM n_a_goods_outwards ngo INNER JOIN n_a_goods g ON ngo.fk_goods = g.idapp INNER JOIN n_a_goods_receive ngr 
    #    ON g.idapp = ngr.fk_goods INNER JOIN n_a_goods_receive_detail grd ON ngr.idapp = grd.fk_app AND ngo.serialnumber = grd.serialnumber LEFT OUTER JOIN 
    #    (SELECT idapp,nik AS used_nik, employee_name AS used_by FROM employee) as empl1 ON empl1.idapp = ngo.fk_employee LEFT OUTER JOIN 
    #    (SELECT idapp AS fk_responsibleperson,nik as resp_nik , employee_name AS empl_resp FROM employee) AS empl2 ON empl2.fk_responsibleperson = ngo.fk_responsibleperson 
    #    WHERE (SELECT COUNT(ngo.idapp))UNION SELECT ngl.idapp, g.itemcode,@table_name := 'GL' AS tbl_name, CONCAT(g.goodsname, ' ',g.brandname, ' ',grd.typeapp) as goods,
    #    grd.serialnumber,empl1.idapp as used_idapp, empl2.fk_responsibleperson,empl1.used_by, empl2.empl_resp, empl1.used_nik, empl2.resp_nik FROM 
    #    n_a_goods_lending ngl INNER JOIN n_a_goods g ON ngl.fk_goods = g.idapp INNER JOIN n_a_goods_receive ngr ON g.idapp = ngr.fk_goods INNER JOIN 
    #    n_a_goods_receive_detail grd ON ngr.idapp = grd.fk_app AND ngl.serialnumber = grd.serialnumber LEFT OUTER JOIN (SELECT idapp,nik AS used_nik,
    #    employee_name AS used_by FROM employee) as empl1 ON empl1.idapp = ngl.fk_employee LEFT OUTER JOIN (SELECT idapp AS fk_responsibleperson,nik as resp_nik , employee_name AS empl_resp FROM employee) 
    #    AS empl2 ON empl2.fk_responsibleperson = ngl.fk_responsibleperson WHERE ngl.status='L') Inner_Tbl)"""
    def searchGoods_byForm(self,data):
        cur = connection.cursor()
        if data['tab_section'] == 'g_outwards':
            Query = """SELECT ngo.idapp,ngo.fk_goods, g.itemcode,CONCAT(g.goodsname, ' ',g.brandname, ' ',grd.typeapp) as goods,@table_name := 'GO' AS tbl_name, ngo.serialnumber,
            empl1.fk_employee,empl1.nik_employee,empl2.fk_resp,empl2.nik_resp FROM n_a_goods_outwards ngo INNER JOIN n_a_goods g ON ngo.fk_goods = g.idapp INNER JOIN n_a_goods_receive ngr 
            ON g.idapp = ngr.fk_goods INNER JOIN n_a_goods_receive_detail grd ON ngr.idapp = grd.fk_app AND ngo.serialnumber = grd.serialnumber
            LEFT OUTER JOIN (SELECT idapp, nik AS nik_employee,employee_name AS fk_employee FROM employee) 
            AS empl1 ON ngo.fk_employee = empl1.idapp LEFT OUTER JOIN (SELECT idapp, nik AS nik_resp,employee_name AS fk_resp FROM employee) AS empl2 ON ngo.fk_responsibleperson = empl2.idapp
            WHERE NOT EXISTS(SELECT m.serialnumber FROM n_a_maintenance m WHERE m.serialnumber=ngo.serialnumber AND m.isfinished=0) AND 
            CONCAT(g.goodsname, ' ',g.brandname, ' ',grd.typeapp) LIKE \'{0}\'"""
            result = 'g_outwards'
        elif data['tab_section'] == 'g_lending':
            Query = """SELECT ngl.idapp,ngl.fk_goods, g.itemcode,CONCAT(g.goodsname, ' ',g.brandname, ' ',grd.typeapp) as goods,ngl.serialnumber,@table_name := 'GL' AS tbl_name,
            empl1.fk_employee,empl1.nik_employee,empl2.fk_resp,empl2.nik_resp FROM n_a_goods_lending ngl INNER JOIN n_a_goods g ON ngl.fk_goods = g.idapp INNER JOIN 
            n_a_goods_receive ngr ON g.idapp = ngr.fk_goods INNER JOIN n_a_goods_receive_detail grd ON ngr.idapp = grd.fk_app AND 
            ngl.serialnumber = grd.serialnumber LEFT OUTER JOIN (SELECT idapp, nik AS nik_employee,employee_name AS fk_employee FROM employee) 
            AS empl1 ON ngl.fk_employee = empl1.idapp LEFT OUTER JOIN (SELECT idapp, nik AS nik_resp,employee_name AS fk_resp FROM employee) AS empl2 ON ngl.fk_responsibleperson = empl2.idapp
            WHERE NOT EXISTS(SELECT gls.idapp FROM n_a_goods_lost gls WHERE gls.serialnumber=ngl.serialnumber) AND CONCAT(g.goodsname, ' ',g.brandname, ' ',grd.typeapp) LIKE \'{0}\'"""
            result = 'g_lending'
        elif data['tab_section'] == 'g_maintenance':
            Query = """SELECT m.idapp, m.fk_goods, g.itemcode, m.fk_goods, m.typeapp, m.serialnumber, @table_name := 'GM' AS tbl_name,
            CONCAT(g.goodsname, ' ', g.brandname, ' ', m.typeapp) AS goods FROM n_a_maintenance m INNER JOIN n_a_goods g ON
            m.fk_goods = g.idapp WHERE NOT EXISTS (SELECT gls.idapp FROM n_a_goods_lost gls WHERE gls.serialnumber=m.serialnumber) AND
            m.isfinished=0 AND CONCAT(g.goodsname, ' ',g.brandname, ' ',m.typeapp) LIKE \'{0}\'"""
            result = 'g_maintenance'
        cur.execute(Query.format('%'+data['goods_filter']+'%'))
        result = (result,query.dictfetchall(cur))
        connection.close()
        return result

    def retriveData(self,idapp):
        cur = connection.cursor()
        if self.dataExist(idapp=idapp):
            Query = """SELECT gls.fk_goods,g.itemcode, CONCAT(g.goodsname, ' ',g.brandname) AS goods, gls.typeApp, gls.serialNumber, empl1.nik_used, empl1.empl_used,empl1.fk_usedemployee,empl2.nik_resp,
            empl2.empl_resp,empl3.fk_lostby,empl3.nik_lostby, empl3.empl_lostby, gls.descriptions FROM n_a_goods_lost gls INNER JOIN n_a_goods g ON 
            gls.fk_goods = g.idapp LEFT OUTER JOIN (SELECT idapp AS fk_usedemployee,nik AS nik_used,employee_name as empl_used FROM employee) AS empl1 ON gls.fk_usedemployee = empl1.fk_usedemployee
            LEFT OUTER JOIN (SELECT idapp, nik AS nik_resp, employee_name AS empl_resp FROM employee) AS empl2 ON gls.fk_responsibleperson = empl2.idapp 
            LEFT OUTER JOIN (SELECT idapp AS fk_lostby, nik AS nik_lostby, employee_name AS empl_lostby FROM employee) AS empl3 ON gls.fk_lostby = empl3.fk_lostby
            WHERE gls.idapp = %s"""
            cur.execute(Query,[idapp])
            result = query.dictfetchall(cur)[0]
            return ('success',result)
        else:
            return ('Lost',)

    def dataExist(self,**kwargs):
        data = super(NA_BR_GoodsLost, self).get_queryset()
        if 'idapp' in kwargs:
            data = data.filter(idapp=kwargs['idapp']).values('idapp')
        if 'serialnumber' in kwargs:
            data = data.filter(serialnumber=kwargs['serialnumber'])
        if 'status' in kwargs:
            data = data.filter(status=kwargs['status'])
        return data.exists()