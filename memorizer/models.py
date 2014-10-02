from google.appengine.ext import ndb


class Receipt(ndb.Model):
	usr = ndb.UserProperty()
	desc = ndb.StringProperty()
	tags = ndb.StringProperty(repeated=True)
	date = ndb.DateTimeProperty(auto_now_add=True)
	picture_dlink = ndb.StringProperty()

	@classmethod
	def listReceiptByUsr(self, user):
		receipts = self.query(self.usr==user).order(-self.date)
		return receipts
