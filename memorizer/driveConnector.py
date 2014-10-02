import httplib2
import pprint
import sys

from apiclient.discovery import build

from oauth2client.appengine import AppAssertionCredentials
from oauth2client.client import HAS_CRYPTO
if HAS_CRYPTO:
  from oauth2client.client import SignedJwtAssertionCredentials
import logging

from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(60)
httplib2.Http(timeout=60)
httplib2.debuglevel = True


# Email of the Service Account.
SERVICE_ACCOUNT_EMAIL = '461408385608-68nkt2854sugji1mkrs82bi9917cbt0p@developer.gserviceaccount.com'

# Path to the Service Account's Private Key file.
SERVICE_ACCOUNT_PKCS12_FILE_PATH = 'privatekey.pem'

API_KEY = 'AIzaSyCLAyxfRw6dXJaiZY62NylLFldf0hYBVSM'

def createDriveService():
  """Builds and returns a Drive service object authorized with the given service account.

  Returns:
    Drive service object.
  """
  f = file(SERVICE_ACCOUNT_PKCS12_FILE_PATH, 'rb')
  key = f.read()
  f.close()

  credentials = SignedJwtAssertionCredentials(SERVICE_ACCOUNT_EMAIL, key,
      scope='https://www.googleapis.com/auth/drive')
  http = httplib2.Http()
  http = credentials.authorize(http)

  return build('drive', 'v2', http=http)

drive_service = createDriveService()

def getDriveServices():
  if drive_service:
    return drive_service
  else:
    return createDriveService()

def print_about(service):
  """Print information about the user along with the Drive API settings.

  Args:
    service: Drive API service instance.
  """
  try:
    about = service.about().get().execute()
    logging.info('Current user name: %s' % about['name'])
    logging.info('Root folder ID: %s' % about['rootFolderId'])
    logging.info('Total quota (bytes): %s' % about['quotaBytesTotal'])
    logging.info('Used quota (bytes): %s' % about['quotaBytesUsed'])
    return about
  except Exception as e:
    logging.error('An error occurred: %s' % e)

def createDriveService1():
  """Builds and returns a Drive service object authorized with the
  application's service account.

  Returns:
    Drive service object.
  """
  credentials = AppAssertionCredentials(
      scope='https://www.googleapis.com/auth/drive')
  http = httplib2.Http()
  http = credentials.authorize(http)

  return build('drive', 'v2', http=http, developerKey=API_KEY)