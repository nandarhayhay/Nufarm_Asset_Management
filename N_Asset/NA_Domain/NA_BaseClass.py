from datetime import date

class NA_Base:
	def __init__(self):
		self.IDApp = 0
		self.CodeApp = ''
		self.NameApp = ''
		self.TypeApp = ''
		self.FKIDApp = 0
		self.FKCodeApp = ''
		self.DescriptionApp = ''
		self.CreatedDate = date.today()
		self.CreatedBy = 'System'
		self.ModifiedDate = date.today()
		self.ModifiedBy = 'System'