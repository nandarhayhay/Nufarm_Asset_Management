from django.db import models, connection,transaction
from NA_DataLayer.common import *
class NA_Acc_FA_BR(models.Manager):
    def PopulateQuery(self,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
        accData = None
        filterfield = columnKey
        if criteria==CriteriaSearch.NotEqual or criteria==CriteriaSearch.NotIn:
            if criteria==CriteriaSearch.NotIn:
                filterfield = columnKey + '__in'
            else:
                filterfield = columnKey + '__iexact'
            accData = super(NA_Acc_FA_BR,self).get_queryset().exclude(**{filterfield:[ValueKey]}).values('idapp','fk_goods','year','startdate','depr_expense','depr_accumulation','bookvalue', 'createddate','createdby')
        if criteria==CriteriaSearch.Equal:
            return super(NA_Acc_FA_BR,self).get_queryset().filter(**{filterfield: ValueKey}).values('idapp','fk_goods','year','startdate','depr_expense','depr_accumulation','bookvalue', 'createddate','createdby')		
        elif criteria==CriteriaSearch.Greater:
            filterfield = columnKey + '__gt'
            accData = super(NA_Acc_FA_BR,self).get_queryset().filter(**{filterfield: ValueKey}).values('idapp','fk_goods','year','startdate','depr_expense','depr_accumulation','bookvalue', 'createddate','createdby')	
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
        elif criteria == CriteriaSearch.Equal:
            filterfield = columnKey + '__exact'
            accData = super(NA_Acc_FA_BR,self).get_queryset().filter(**{filterfield: [ValueKey] if filterfield == (columnKey + '__in') else ValueKey})	
        if criteria==CriteriaSearch.Beetween or criteria==CriteriaSearch.BeginWith or criteria==CriteriaSearch.EndWith:
            rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)			
            accData = super(NA_Acc_FA_BR,self).get_queryset().select_related('fk_goods').filter(**rs.DefaultModel())

        accData = accData.values('idapp','fk_goods','year','startdate','depr_expense','depr_accumulation','bookvalue', 'createddate','createdby')
        return accData

    def create_acc_FA(self,**data):
        with transaction.atomic():
    #        q = '''INSERT INTO n_a_acc_fa(FK_Goods,Year,StartDate,Depr_Expense,Depr_Accumulation,BookValue,CreatedDate,CreatedBy)
    #        values(%s,%s,%s,%s,%s,%s,%s,%s)'''
    #        prms = [data['fk_goods'],data['year'],data['startdate'],data['depr_expense'],\
				#data['depr_accumulation'],data['bookvalue'],data['createddate'],data['createdby']]
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO n_a_acc_fa(FK_Goods,Year,StartDate,Depr_Expense,Depr_Accumulation,BookValue,CreatedDate,CreatedBy)
            values(%s,%s,%s,%s,%s,%s,%s,%s)''',[
                data['fk_goods'],data['year'],data['startdate'],data['depr_expense'],
				data['depr_accumulation'],data['bookvalue'],data['createddate'],data['createdby']
                ]
            )
            row = cursor.fetchone()
            return row