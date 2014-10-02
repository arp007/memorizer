import os
import urllib


from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from models import Receipt
from google.appengine.ext import ndb
import webapp2
import jinja2
import logging
import mimetypes
from driveUtil import insert_file, getFilesList, insert_permission, getFileInfoById, downloadFile
import cgi

JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True,
	)
from util import datetimeformat
JINJA_ENVIRONMENT.filters['date'] = datetimeformat

class BaseRequestHandler(webapp2.RequestHandler):
	

	def renderTemplate(self, template_location):
		template = JINJA_ENVIRONMENT.get_template(template_location)
		return template



class MainPage(BaseRequestHandler):
	def get(self):
		
		#check for the active google account session
		user = users.get_current_user()
		if user:
			upload_url = "/upload"
			template_values = {
			    'name' : user.nickname(),
			    'upload_url' : upload_url
			    }
			template = self.renderTemplate('templates/index.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect(users.create_login_url(self.request.uri))


class Info(webapp2.RequestHandler):
	def get(self):
		file_list = getFilesList()
		items = file_list.get('items')
		for item in items:
			print item
		insert_permission(service, '0B802SdLOxiyyTVVBSEtaT2tYTkk', 'rajanishpoudel@gmail.com','user','reader')


class UploadFileToDriveHandler(webapp2.RequestHandler):
	def post(self):
		user = users.get_current_user()
		if user:
			try:
				file_upload = self.request.POST.get("file", None)
				file_name = file_upload.filename
				logging.info(file_name)
				file = insert_file(file_name,"Image file",None, mimetypes.guess_type(file_name)[0],file_upload.file.read())
				insert_permission(file.get('id'), 'rajanishpoudel@gmail.com','user','reader')
				receipt = Receipt()
				receipt.desc = self.request.get('desc')
				receipt.tags = self.request.get('tags').split()
				receipt.usr = user
				receipt.picture_dlink = file.get('id')
				receipt.put()
				self.response.write(JINJA_ENVIRONMENT.get_template('templates/submit_success.html').render({'id' : file.get('id')}))
			except Exception as e:
				self.response.write("Sorry, something went wrong. Please try again later!!")
				logging.error(e)
		else:
			self.redirect(users.create_login_url(self.request.uri))

class ServeFileFromDrive(webapp2.RequestHandler):
	def get(self, file_id):
		drive_file = getFileInfoById(file_id)
		file_content = downloadFile(drive_file)
		self.response.headers[b'Content-Type'] = mimetypes.guess_type(drive_file.get('title'))[0]
		self.response.write(file_content)

class ListReceipt(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			list_receipt = Receipt.listReceiptByUsr(user)
			self.response.write(JINJA_ENVIRONMENT.get_template('templates/list_new.html').render({'receipts' : list_receipt}))
			

		else:
			self.redirect(users.create_login_url(self.request.uri))


application = webapp2.WSGIApplication(
	[
	('/', MainPage),
	('/upload', UploadFileToDriveHandler),
	('/servefile/([^/]+)?', ServeFileFromDrive),
	('/info', Info),
	('/list', ListReceipt)
	],debug =  True)