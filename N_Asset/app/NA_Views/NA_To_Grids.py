from .jqgrid import JqGrid
from NA_Models.models import Employee, NASuplier

class EmployeeGrid(JqGrid):
    queryset = Employee.objects.all()

class NA_SuplierGrid(JqGrid):
    queryset = NASuplier.objects.all()