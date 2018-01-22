from enum import Enum
from datetime import date
from datetime import datetime
class CriteriaSearch(Enum):
	Equal = 1
	BeginWith = 2
	EndWith = 3
	NotEqual = 4
	Greater = 5
	Less = 6
	LessOrEqual = 7
	GreaterOrEqual = 8
	Like = 9
	In = 10
	NotIn = 11
	Beetween = 12
class StatusForm(Enum):
	Input = 1
	Edit = 2; InputOrEdit = 3; View = 4; 
class DataType(Enum):
	  BigInt = 1; Boolean = 2;Char = 3;DateTime = 4; Decimal = 5; Float = 6; Image = 7; Integer = 8;
	  Money = 9; NChar = 10; NVarChar = 11; VarChar = 12; Variant=13;

class ResolveCriteria:
	__query = "";
	def __init__(self,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar,columnKey='',value=None):
		self.criteria = criteria
		self.typeofData = typeofData
		self.valueData = value
		self.colKey = columnKey
	def DefaultModel(self):
		filterfield = colKey + '__istarswith'
		if self.criteria==CriteriaSearch.Beetween:
			if typeofData==DataType.Boolean or typeofData==DataType.Char or typeofData==DataType.NChar or typeofData==DataType.NVarChar \
				or typeofData==DataType.VarChar:
					raise ValueError('value type is in valid')
			if typeofData==DataType.DateTime:
				if ',' in str(valueData):
					strValueKeys = str(valueData).split(',')
					filterfield = colKey + '__range'
					return {filterfield:[datetime((str(strValueKeys[0])[0:3]),str(strValueKeys[0])[5:6],str(strValueKeys[0])[7:8]),datetime((str(strValueKeys[1])[0:3]),str(strValueKeys[1])[5:6],str(strValueKeys[1])[7:8])]}
			elif typeofData==DataType.BigInt or typeofData==DataType.Decimal or typeofData==DataType.Float or typeofData==DataType.Integer or typeofData==DataType.Money:
				return {filterfield:[valueData[0],valueData[1]]}
			else:
				raise ValueError('value type is in valid')
		elif self.criteria==CriteriaSearch.BeginWith:
			if typeofData==DataType.Char or typeofData==DataType.VarChar or typeofData==DataType.NVarChar:
				return {filterfield:valueData}
			else:
				raise ValueError('value type is in valid')
		elif self.criteria==CriteriaSearch.EndWith:
			if typeofData==DataType.Char or typeofData==DataType.VarChar or typeofData==DataType.NVarChar:
				filterfield = colKey + '__iendswith'
			else:
				raise ValueError('value type is in valid')
			return {filterfield:valueData}

	def Sql(self):
		if self.criteria==CriteriaSearch.Beetween:
			if typeofData==DataType.Boolean or typeofData==DataType.Char or typeofData==DataType.NChar or typeofData==DataType.NVarChar \
				or typeofData==DataType.VarChar:
					raise ValueError('value type is in valid')
			if typeofData==DataType.DateTime:
				values = str(valueData).split('-')
				startDate = values[0]
				endDate = values[1]
				__query = ' >= {0!s} AND ' + colKey + ' <= {1!s}'.format(startDate,endDate)
		elif self.criteria==CriteriaSearch.BeginWith:
			if typeofData==DataType.Char or typeofData==DataType.VarChar or typeofData==DataType.NVarChar:
				__query = ' LIKE {0!s}%'.format(str(valueData))
		elif self.criteria==CriteriaSearch.EndWith:
			if typeofData==DataType.Char or typeofData==DataType.VarChar or typeofData==DataType.NVarChar:
				__query = ' LIKE %{0!s}'.format(str(valueData))
		elif self.criteria == CriteriaSearch.Equal:
			__query = ' = {0}'.format(valueData)
		elif self.criteria==CriteriaSearch.Greater:
			if typeofData==DataType.Integer or typeOfData== DataType.Decimal or typeofData==DataType.Float or typeofData==DataType.Money \
				or typeofData==DataType.BigInt:
				__query = ' > {0}'.format(float(valueData))
			elif typeofData==DataType.DateTime:
				__query = ' > {%Y-%m-%d}'.format(datetime((str(valueData)[0:3]),str(valueData)[5:6],str(valueData)[7:8]))
		elif self.criteria==CriteriaSearch.GreaterOrEqual:
			if typeofData==DataType.Integer or typeOfData== DataType.Decimal or typeofData==DataType.Float or typeofData==DataType.Money \
				or typeofData==DataType.BigInt:
				__query = ' > {0}'.format(float(valueData))
			elif typeofData==DataType.DateTime:
				#format data yang di masukan di valueData mesti dijadikan tahun-bulan-tanggal sebelum di proses
				__query = ' >= {%Y-%m-%d}'.format(datetime((str(valueData)[0:3]),str(valueData)[5:6],str(valueData)[7:8]))
		elif self.criteria==CriteriaSearch.In:
			if ',' in str(valueData):
				strValueKeys = str(valueData).split(',')
				rowFilter = " IN('"
				for i in range(len(strValueKeys)):
					rowFilter += strValueKeys[i] + "'"
					if i < len(strValueKeys) -1:
						rowFilter += ","
				rowFilter += ")"
			if typeofData==DataType.Char or typeofData==DataType.VarChar or typeofData==DataType.NVarChar:
				if rowFilter != " IN(')":
					__query = rowFilter
				else:
					__query = " IN ('{0!s}')".format(str(valueData))
			elif typeofData==DataType.DateTime:
			#format data yang di masukan di valueData mesti dijadikan tahun-bulan-tanggal sebelum di proses	
				__query = ' IN {%Y-%m-%d}'.format(datetime((str(valueData)[0:3]),str(valueData)[5:6],str(valueData)[7:8]))
		elif self.criteria==CriteriaSearch.Less:
			if typeofData==DataType.Integer or typeOfData== DataType.Decimal or typeofData==DataType.Float or typeofData==DataType.Money \
				or typeofData==DataType.BigInt:
				__query = ' < {0}'.format(float(valueData))
			elif typeofData==DataType.DateTime:
				__query = ' < {%Y-%m-%d}'.format(datetime((str(valueData)[0:3]),str(valueData)[5:6],str(valueData)[7:8]))
		elif self.criteria==CriteriaSearch.LessOrEqual:
			if typeofData==DataType.Integer or typeOfData== DataType.Decimal or typeofData==DataType.Float or typeofData==DataType.Money \
				or typeofData==DataType.BigInt:
				__query = ' <= {0}'.format(float(valueData))
			elif typeofData==DataType.DateTime:
				__query = ' <= {%Y-%m-%d}'.format(datetime((str(valueData)[0:3]),str(valueData)[5:6],str(valueData)[7:8]))
		elif self.criteria==CriteriaSearch.Like:
			if typeofData==DataType.Char or typeofData==DataType.VarChar or typeofData==DataType.NVarChar:
				__query = ' LIKE %{0!s}%'.format(str(valueData))
		elif self.criteria==CriteriaSearch.NotEqual:
				__query = ' <>{0} '.format(str(valueData))

	def getDataType(strDataType):
		if strDataType=='varchar':
			return DataType.VarChar
		elif strDataType == 'bigint':
			return DataType.BigInt
		elif strDataType == 'boolean':
			return DataType.Boolean
		elif strDataType == 'char':
			return DataType.Char
		elif strDataType == 'datetime':
			return DataType.DateTime
		elif strDataType == 'decimal':
			return DataType.Decimal
		elif strDataType == 'float':
			return DataType.Float
		elif strDataType == 'image':
			return DataType.Image
		elif strDataType == 'money':
			return DataType.Money
		elif strDataType == 'nchar':
			return DataType.Char
		elif strDataType =='nvarchar':
			return DataType.NVarChar
		else :
			return DataType.VarChar
	
	def getCriteriaSearch(strCriteria):
		if strCriteria == 'equal':
			return CriteriaSearch.Equal
		elif strCriteria == 'beginwith':
			return CriteriaSearch.BeginWith
		elif strCriteria == 'endwith':
			return CriteriaSearch.EndWith
		elif strCriteria == 'notequal':
			return CriteriaSearch.NotEqual
		elif strCriteria == 'greater':
			return CriteriaSearch.Greater
		elif strCriteria == 'less':
			return CriteriaSearch.Less
		elif CriteriaSearch == 'lessorequal':
			return CriteriaSearch.LessOrEqual
		elif strCriteria == 'greaterorequal':
			return CriteriaSearch.GreaterOrEqual
		elif strCriteria == 'like':
			return CriteriaSearch.Like
		elif strCriteria == 'in':
			return CriteriaSearch.In
		elif strCriteria == 'notin':
			return CriteriaSearch.NotIn
		elif strCriteria == 'beetween':
			return CriteriaSearch.Beetween
		else:
			return CriteriaSearch.Like
class decorators:
	def ajax_required(f):
		def wrap(request, *args, **kwargs):
			if not request.is_ajax():
				return HttpResponseBadRequest()
			return f(request, *args, **kwargs)
			wrap.__doc__=f.__doc__
			wrap.__name__=f.__name__
			return wrap
class query:
	def dictfetchall(cursor):
		"Return all rows from a cursor as a dict"
		columns = [col[0] for col in cursor.description]
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]