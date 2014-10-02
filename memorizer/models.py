from google.appengine.ext import ndb

class Images(ndb.Model):
	filename = ndb.StringProperty()
	blob = ndb.BlobProperty()

class Receipt(ndb.Model):
	usr = ndb.UserProperty()
	desc = ndb.StringProperty()
	tags = ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)
	picture = ndb.KeyProperty(kind=Images)
	picture_dlink = ndb.StringProperty()

	@classmethod
	def listReceiptByUsr(self, user):
		receipts = self.query(self.usr==user).order(-self.date)
		return receipts
