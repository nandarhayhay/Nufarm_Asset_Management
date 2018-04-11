from django.db import models, connection, transaction
from NA_DataLayer.common import CriteriaSearch, DataType, StatusForm, ResolveCriteria
from django.db.models import Q
from datetime import datetime

class NA_BR_Suplier(models.Manager):
    def PopulateQuery(self,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
        suplierData = None
        filterfield = columnKey
        if criteria==CriteriaSearch.NotEqual or criteria==CriteriaSearch.NotIn:
            if criteria==CriteriaSearch.NotIn:
                filterfield = columnKey + '__in'
            else:
                filterfield = columnKey + '__iexact'
            suplierData = super(NA_BR_Suplier,self).get_queryset().exclude(**{filterfield:[ValueKey]})
        if criteria==CriteriaSearch.Equal:
            return super(NA_BR_Suplier,self).get_queryset().filter(**{filterfield: ValueKey})
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
            filterfield = columnKey + '__contains'
            suplierData = super(NA_BR_Suplier,self).get_queryset().filter(**{filterfield: [ValueKey] if filterfield == (columnKey + '__in') else ValueKey})	
        if criteria==CriteriaSearch.Beetween or criteria==CriteriaSearch.BeginWith or criteria==CriteriaSearch.EndWith:
            rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)			
            suplierData = super(NA_BR_Suplier,self).get_queryset().filter(**rs.DefaultModel())

        suplierData = suplierData.values('supliercode','supliername','address','telp','hp','contactperson','inactive','createddate','createdby')				
        return suplierData

    def SaveData(self, statusForm, **data):
        cur = connection.cursor()
        Params = {'supliercode':data['supliercode'], 'supliername':data['supliername'], 'address':data['address'], 'telp':data['telp'],\
            'hp':data['hp'], 'contactperson':data['contactperson'], 'inactive':data['inactive']}
        if statusForm == StatusForm.Input:
            check_exists = self.dataExist(supliercode=data['supliercode'],hp=data['hp'],telp=data['telp'])
            if check_exists[0]:
                return ('exists',check_exists[1])
            else:
                Query = '''INSERT INTO n_a_suplier(SuplierCode, SuplierName, Address, Telp, Hp, ContactPerson, Inactive, CreatedDate, CreatedBy)
                values(%(supliercode)s,%(supliername)s,%(address)s,%(telp)s,%(hp)s,%(contactperson)s,%(inactive)s,%(createddate)s,%(createdby)s)'''
                Params['createddate'] = data['createddate']
                Params['createdby'] = data['createdby']
        elif statusForm == StatusForm.Edit:
            if self.HasRef(data['supliercode']):
                return 'hasref'
            else:
                check_exists = self.dataExist(hp=data['hp'],telp=data['telp'])
                if check_exists[0]:
                    return ('exists',check_exists[1])
                else:
                    Params['modifieddate'] = data['modifieddate']
                    Params['modifiedby'] = data['modifiedby']
                    Query = """UPDATE n_a_suplier SET SuplierName=%(supliername)s, Address=%(address)s, Telp=%(telp)s, Hp=%(hp)s, 
                    ContactPerson=%(contactperson)s, Inactive=%(inactive)s,ModifiedDate=%(modifieddate)s, ModifiedBy=%(modifiedby)s 
                    WHERE SuplierCode=%(supliercode)s"""
        cur.execute(Query,Params)
        rowId = cur.lastrowid
        connection.close()
        return (rowId,)

    def delete_suplier(self,**kwargs):
        cur = connection.cursor()
        supliercode = kwargs['supliercode']
        check_exists = self.dataExist(supliercode=supliercode)
        if check_exists[0]:
            if self.HasRef(supliercode):
                return 'HasRef'
            else:
                data = self.retriveData(supliercode)[1][0] #tuple
                createddate = data['createddate']
                modifieddate = data.get('modifieddate')
                if isinstance(createddate,datetime):
                    data['createddate'] = createddate.strftime('%d %B %Y %H:%M:%S')
                dataPrms = {'SuplierCode':data['supliercode'],'SuplierName':data['supliername'],'Address':data['address'],'Telp':data['telp'],
                            'Hp':data['hp'],'ContactPerson':data['contactperson'],
                            'Inactive':data['inactive'],'CreatedDate':data['createddate'],'CreatedBy':data['createdby']}
                #============== INSERT TO LOG EVENT ===============
                Query = """INSERT INTO logevent(nameapp,descriptions,createddate,createdby) VALUES(\'Deleted Suplier\',JSON_OBJECT(\'deleted\',
                        JSON_ARRAY(%(SuplierCode)s,%(SuplierName)s,%(Address)s,%(Telp)s,%(Hp)s,%(ContactPerson)s,%(Inactive)s,
                        %(CreatedDate)s,%(CreatedBy)s"""
                if modifieddate is not None:
                    if isinstance(modifieddate,datetime):
                        data['modifieddate'] = modifieddate.strftime('%d %B %Y %H:%M:%S')
                    dataPrms['ModifiedDate'] = modifieddate
                    dataPrms['ModifiedBy'] = data['modifiedby']
                    Query = Query + """,%(ModifiedDate)s,%(ModifiedBy)s"""
                Query = Query + """)),NOW(),%(NA_User)s)"""
                try:
                    with transaction.atomic():
                        NA_User = 'Admin'
                        if 'NA_User' in kwargs:
                            NA_User = kwargs['NA_User']
                        dataPrms['NA_User'] = NA_User
                        cur.execute(Query,dataPrms)
                        #================= END INSERT LOG EVENT ===============
                        cur.execute("""DELETE FROM n_a_suplier where SuplierCode=%s""",[supliercode])
                except Exception:
                    transaction.rollback()
                    connection.close()
                    raise
                connection.close()
                return 'success'
        else:
            return 'Lost'
    def retriveData(self, get_supliercode):
        if self.dataExist(supliercode=get_supliercode):
            result = super(NA_BR_Suplier, self).get_queryset()\
                .filter(supliercode=get_supliercode).values(
                    'supliercode','supliername','address','telp','hp',
                    'contactperson','inactive','createddate','createdby')
            return ('success',result)
        else:
            return ('Lost',)

    def dataExist(self, **kwargs):
        data = super(NA_BR_Suplier,self).get_queryset()
        if 'supliercode' in kwargs:
            suplier_code = kwargs['supliercode']
            exist_supCode = data.filter(supliercode=suplier_code).exists()
            if exist_supCode:
                return (True,'Suplier with suplier code {0} has exists'.format(suplier_code))
        if 'hp' in kwargs and 'telp' in kwargs:
            sup_code = kwargs.get('sup_code_exclude')
            if sup_code == None and 'supliercode' in kwargs:
                sup_code = kwargs['supliercode']
            exist_hp = data.exclude(supliercode=sup_code).filter(hp=kwargs['hp']).exists()
            if exist_hp:
                return (True,'Suplier with Hp {0} has exists'.format(kwargs['hp']))
            exist_telp = data.exclude(supliercode=sup_code).filter(telp=kwargs['telp']).exists()
            if exist_telp:
                return (True,'Suplier with Telp {0} has exists'.format(kwargs['telp']))
        return (False,)
    def HasRef(self,supCode):
        cur = connection.cursor()
        Query = '''SELECT EXISTS(SELECT FK_Suplier FROM n_a_goods_receive WHERE FK_Suplier=%(supliercode)s)'''
        Params = {'supliercode':supCode}
        cur.execute(Query,Params)
        if cur.fetchone()[0] > 0:
            return True
        else:
            return False
