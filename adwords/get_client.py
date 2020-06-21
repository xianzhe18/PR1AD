from google.ads.google_ads.client import GoogleAdsClient
import os
from django.conf import settings

def get_client():
    path = os.path.join(settings.BASE_DIR, 'static')
    client = GoogleAdsClient.load_from_storage(path+'/google-ads.yaml')
    return client

def adwords_client():
    path = os.path.join(settings.BASE_DIR, 'static')
    adwords_client = adwords.AdWordsClient.LoadFromStorage(path+'/google-ads.yaml')
    return adwords_client