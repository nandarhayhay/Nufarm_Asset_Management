from django.db import models, connection
from NA_DataLayer.common import *

class NA_BR_Suplier(models.Manager):
    def PopulateQuery(self,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
        suplierData = None
        filterfield = columnKey
        if criteria==CriteriaSearch.NotEqual or criteria==CriteriaSearch.NotIn:
            if criteria==CriteriaSearch.NotIn:
                filterfield = columnKey + '__in'
            else:
                filterfield = columnKey + '__iexact'
            suplierData = super(NA_BR_Suplier,self).get_queryset().exclude(**{filterfield:[ValueKey]}).values('supliercode','supliername','address','telp','hp','contactperson','inactive','createddate','createdby')	
        if criteria==CriteriaSearch.Equal:
            return super(NA_BR_Suplier,self).get_queryset().filter(**{filterfield: ValueKey}).values('supliercode','supliername','address','telp','hp','contactperson','inactive','createddate','createdby')		
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


    def create_suplier(self, **data):
        suplier = self.create(
            supliercode=data['supliercode'],
            supliername=data['supliername'],
            address=data['address'],
            telp=data['telp'],
            hp=data['hp'],
            contactperson=data['contactperson'],
            inactive=data['inactive'],
            createddate=data['createddate'],
            createdby=data['createdby']
            )
        return suplier.supliercode


    #def create_suplier(self, **data):
    #    cursor = connection.cursor()
    #    cursor.execute('''INSERT INTO n_a_suplier(SuplierCode, SuplierName, Address, Telp, Hp, ContactPerson, Inactive, CreatedDate, CreatedBy)
    #    values(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',[
    #        data['supliercode'], data['supliername'], data['address'], data['telp'], data['hp'], data['contactperson'], data['inactive'], data['createddate'], data['createdby']]
    #    )

    #    row = cursor.fetchone()
    #    connection.close()
    #    return row

    def update_suplier(self, **data):
        cursor = connection.cursor()
        cursor.execute('''UPDATE n_a_suplier SET
        SuplierName=%s, Address=%s, Telp=%s, Hp=%s, ContactPerson=%s, Inactive=%s, ModifiedDate=%s, ModifiedBy=%s where SuplierCode=%s
        ''',[
            data['supliername'], data['address'], data['telp'], data['hp'], data['contactperson'], data['inactive'], data['modifieddate'], data['modifiedby'], data['supliercode']]
        )

        row = cursor.fetchone()
        connection.close()
        return row

    def delete_suplier(self, get_supcode):
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM n_a_suplier where SuplierCode=%s
        ''',[get_supcode]
        )

        row = cursor.fetchone()
        connection.close()
        return row
    def retriveData(self, get_supliercode):
        return super(NA_BR_Suplier, self).get_queryset().filter(supliercode=get_supliercode)

    def dataExist(self, get_supliercode):
        return super(NA_BR_Suplier, self).get_queryset().filter(supliercode=get_supliercode).exists()