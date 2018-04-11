from django.db import models, connection
from NA_DataLayer.common import *

class NA_BR_Employee(models.Manager):
    def PopulateQuery(self,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
        employeeData = None
        filterfield = columnKey
        if criteria==CriteriaSearch.NotEqual or criteria==CriteriaSearch.NotIn:
            if criteria==CriteriaSearch.NotIn:
                filterfield = columnKey + '__in'
            else:
                filterfield = columnKey + '__iexact'
            employeeData = super(NA_BR_Employee,self).get_queryset().exclude(**{filterfield:[ValueKey]}).values('idapp','nik','employee_name','typeapp','jobtype','gender','status','telphp','territory','descriptions','inactive','createddate','createdby')	
        if criteria==CriteriaSearch.Equal:
            return super(NA_BR_Employee,self).get_queryset().filter(**{filterfield: ValueKey}).values('idapp','nik','employee_name','typeapp','jobtype','gender','status','telphp','territory','descriptions','inactive','createddate','createdby')		
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
            employeeData = super(NA_BR_Employee,self).get_queryset().filter(**{filterfield: [ValueKey] if filterfield == (columnKey + '__in') else ValueKey})	
        if criteria==CriteriaSearch.Beetween or criteria==CriteriaSearch.BeginWith or criteria==CriteriaSearch.EndWith:
            rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)			
            employeeData = super(NA_BR_Employee,self).get_queryset().filter(**rs.DefaultModel())

        employeeData = employeeData.values('idapp','nik','employee_name','typeapp','jobtype','gender','status','telphp','territory','descriptions','inactive','createddate','createdby')				
        return employeeData


    def create_employee(self, **data):
        employee = self.create(
            nik=data['nik'],
            employee_name=data['employee_name'],
            typeapp=data['typeapp'],
            jobtype=data['jobtype'],
            gender=data['gender'],
            status=data['status'],
            telphp=data['telphp'],
            territory=data['territory'],
            descriptions=data['descriptions'],
            inactive=data['inactive'],
            createddate=data['createddate'],
            createdby=data['createdby']
            )
        return employee.idapp

    #def create_employee(self, **data):
    #    cursor = connection.cursor()
    #    cursor.execute('''INSERT INTO employee(nik, employee_name, typeapp, jobtype, gender,
    #    status, telphp, territory, descriptions, inactive,createddate, createdby)
    #    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', [
    #        data['nik'], data['employee_name'], data['typeapp'], data['jobtype'], data['gender'], data['status'], data['telphp'],
    #        data['territory'], data['descriptions'], data['inactive'],data['createddate'], data['createdby']]
    #        )
    #    row = cursor.fetchone()
    #    connection.close()
    #    return row


        #def SaveData(self,statusForm=StatusForm.Input,**data):
        #cursor = connection.cursor()
        #Params = {'Nik':data['nik'],'Employee_Name':data['employee_name'],'TypeApp':data['typeapp'],'JobType':data['jobtype']}
        #if statusForm == StatusForm.Input:
        #    cursor.execute('''INSERT INTO employee(nik, employee_name, typeapp, jobtype, gender,
        #    status, telphp, territory, descriptions, inactive,createddate, createdby)
        #    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', [
        #        data['nik'], data['employee_name'], data['typeapp'], data['jobtype'], data['gender'], data['status'], data['telphp'],
        #        data['territory'], data['descriptions'], data['inactive'],data['createddate'], data['createdby']]
        #        )
        #elif statusForm == StatusForm.Edit:
        #    Query = '''UPDATE employee SET nik=%s,employee_name=%s, typeapp=%s, 
        #    jobtype=%s, gender=%s, status=%s, telphp=%s, territory=%s,
        #    descriptions=%s, inactive=%s, modifieddate=%s, modifiedby=%s WHERE idapp=%s'''
        #    cursor.execute(Query,[
        #        data['nik'], data['employee_name'], data['typeapp'], data['jobtype'], data['gender'], data['status'], data['telphp'],
        #        data['territory'], data['descriptions'], data['inactive'], data['modifieddate'],data['modifiedby'], data['idapp']
        #        ]
        #            )
        #row = cursor.fetchone()
        #connection.close()
        #return row


    def update_employee(self, **data):
        cursor = connection.cursor()
        Query = '''UPDATE employee SET nik=%s,employee_name=%s, typeapp=%s, 
        jobtype=%s, gender=%s, status=%s, telphp=%s, territory=%s,
        descriptions=%s, inactive=%s, modifieddate=%s, modifiedby=%s WHERE idapp=%s'''
        cursor.execute(Query,[
            data['nik'], data['employee_name'], data['typeapp'], data['jobtype'], data['gender'], data['status'], data['telphp'],
            data['territory'], data['descriptions'], data['inactive'], data['modifieddate'],data['modifiedby'], data['idapp']
            ]
                )
        row = cursor.fetchone()
        connection.close()
        return row

    def delete_employee(self, get_idapp):
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM employee where idapp=%s
        ''',[get_idapp]
        )
        row = cursor.fetchone()
        connection.close()
        return row

    def retriveData(self, get_idapp):
        return super(NA_BR_Employee, self).get_queryset().filter(idapp__exact=get_idapp)

    def dataExist(self, get_nik):
        return super(NA_BR_Employee, self).get_queryset().filter(nik=get_nik).exists()