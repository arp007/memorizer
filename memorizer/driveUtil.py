from apiclient import errors
from apiclient.http import MediaFileUpload, MediaInMemoryUpload
import logging
from driveConnector import getDriveServices

def insert_file(title, description, parent_id, mime_type, file_data):
	media_body = MediaInMemoryUpload(file_data, mime_type or file_data.content_type, resumable=True)
	body ={
		'title' : title,
		'description' : description,
		'mime_type' : mime_type
	}
	# setting the parent folder
	if parent_id:
		body['parents'] = [{'id':parent_id}]

	try:
		file = getDriveServices().files().insert(
			body=body,
			media_body = media_body
			).execute()
		logging.info("File is %s"%file['id'])
		return file
	except errors.HttpError, error:
		logging.error('An error occured: %s'%error)
		return None

def getFilesList():
	return getDriveServices().files().list().execute()

def getFileInfoById(file_id):
	try:
		file = getDriveServices().files().get(fileId=file_id).execute()
		logging.info("File title %s"%file.get('title'))
		logging.info('File MIME: %s'%file.get('mimeType'))
		return file
	except errors.HttpError, error:
		logging.error(error)

def downloadFile(drive_file):
	download_url = drive_file.get('downloadUrl')
	if download_url:
		resp, content = getDriveServices()._http.request(download_url)
		if resp.status == 200:
			logging.info('Status: %s'%resp.status)
			return content
		else:
			logging.error('An error occured: %s'% resp)
			return None




def insert_permission(file_id, value, perm_type, role):
	new_permission = {
		'value': value,
		'type' : perm_type,
		'role' : role
	}
	try:
		perm =  getDriveServices().permissions().insert(
			fileId = file_id, body= new_permission).execute()
		print "perm is "
		print perm
	except errors.HttpError, error:
		print 'An error occured: %s'% error
		return None

