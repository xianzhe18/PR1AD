import argparse

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPE = u'https://www.googleapis.com/auth/adwords'
import os
from django.conf import settings

def authenticate():
    path = os.path.join(settings.BASE_DIR, 'static')
    flow = InstalledAppFlow.from_client_secrets_file(
        path+'/creds.json', scopes=[SCOPE])

    flow.run_local_server()

    print('Access token: %s' % flow.credentials.token)
    print('Refresh token: %s' % flow.credentials.refresh_token)
