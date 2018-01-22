from NA_Domain.NA_BaseClass import  NA_Base
from datetime import datetime

class C_Goods(NA_Base):
	def __init__(self,BrandName='',PricePerunit=0,DeprMethod='SL',Unit='Pcs',EconomicLife=5,Placement='Gudang IT1',InActive=0):
		NA_Base.__init__()
		self.brandName = BrandName
		self.pricePerUnit = PricePerunit
		self.depreciationMethod = DeprMethod
		self.unit = Unit
		self.economicLife = EconomicLife
		self.placement = Placement
		self.inActive = InActive
class Goods_Return(C_Goods):
	def __init__(self,DateReturn=datetime.now(),Condition='B',FromEmployee='',UsedEmployee='',IsCompleted=1,Minus=0,FK_Lend=0,FK_GoodsOutWards=0):
		Goods.__init__()
		self.dateReturn = DateReturn
		self.condition = Condition
		self.fromEmployee = FromEmployee
		self.UsedEmployee = UsedEmployee
		self.isCompleted = IsCompleted
		self.minus = Minus
		self.fk_lend = FK_Lend
		self.fk_goodsOutwards = FK_GoodsOutWards

class Goods_Outwards(C_Goods):
	def __init__(self,Qty=0,DateRequest=datetime.now(),DateReleased=datetime.now(),FK_Employee='',FK_UsedEmployee='',FK_FromMaintain='',FKResponsiblePerson='',FK_Sender='',FK_Stock=''):
		Goods.__init__()
		self.dateRequest = DateRequest
		self.dateReleased = DateReleased
		self.fk_employee = FK_Employee
		self.fk_usedEmployee = FK_UsedEmployee
		self.fk_fromMaintain= FK_FromMaintain
		self.fk_sender = FK_Sender
		self.fk_responsiblePerson = FKResponsiblePerson
		self.sk_stock = FK_Stock
