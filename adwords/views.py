from django.shortcuts import render, HttpResponse, redirect
import argparse
from .get_client import get_client
from google_auth_oauthlib.flow import InstalledAppFlow
import argparse
import datetime
import sys
import uuid
import google.ads.google_ads.client
from adwords import models
from django.conf import settings
import os
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
import datetime

from adwords.authenticate import authenticate
from adwords.ads_report import ads_report
from adwords.get_campaign import get_campaign

from django.views.decorators.clickjacking import xframe_options_exempt
import uuid
from googleads import adwords
GOOGLE_RECAPTCHA_SECRET_KEY = 'private-key'

_DATE_FORMAT = '%Y%m%d'
# from .get_campaign import get_campaign
# get_campaign()

def index(request):
    user = request.user.username
    m = models.ads_model.objects.filter(created_by=user)
    if m:
        return render(request, 'index.html', {'ads_models': m})
    else:
        return render(request, 'index.html')

@xframe_options_exempt
def ads_model_details(request, c_id):
    try:
        ads_model_details = models.ads_model.objects.get(pk=c_id)
        return render(request, 'ads_model_details.html', {'c': ads_model_details})
    except ObjectDoesNotExist:
        error = "This ads_model Does Not Exists"
        return render(request, 'ads_model_details.html', {'e': error})    

def approve_ads_models(request, c_id):
    try:
        m = models.ads_model.objects.get(model_id=c_id)
        if m.update_pending == 1:
            m.update_pending = 0
            m.pause = 0
            m.approved = 1
        else:
            m.approved = 1
            m.pause = 0
        m.save()
        return ads_model_details(request, c_id)
    except (ObjectDoesNotExist, EOFError):
        error = "Some Unknown Error Occured"
        return render(request, 'ads_model_details.html', {'e': error})

def enable(request, c_id):
    try:
        m = models.ads_model.objects.get(model_id=c_id)
        m.pause = 0
        m.approved = 1
        m.save()
        return ads_model_details(request, c_id)
    except ObjectDoesNotExist:
        error = "This ads_model Does Not Exists"
        return render(request, 'ads_model_details.html', {'e': error})    

def all_ads_models(request):
    m = models.ads_model.objects.all()
    if m:
        data = {
            'ads_models': m
        }
        return render(request, 'ads_models.html', data)
    else:
        return render(request, 'ads_models.html')


def reports(request, c_id):
    r = ads_report(c_id)
    data = {
        'cpm': r.cpm,
        'cpv': r.cpv,
        'cost': r.cost
    }
    return render(request, 'reports.html', data)

def pause_ads_models(request, c_id):
    m = models.ads_model.objects.get(model_id=c_id)
    m.pause = 1
    m.approved = 0
    m.save()
    return ads_model_details(request, c_id)

def delete_ads_models(request, c_id):
    c = models.ads_model.objects.get(model_id=c_id)
    c.delete()
    return redirect("adwords:all_campaigns")

def edit_ads_models(request, c_id):
    return render(request, 'index.html', {'model': c_id})


class Create_ads_models(View):
    def post(self, *args, **kwargs):
        user = self.request.user.username
        model_id = self.request.POST['model_id'] or None
        ad_name = self.request.POST['ad_name']
        keywords = self.request.POST['keywords']
        cpv_bid = self.request.POST.get('cpv_bid')
        video_url = self.request.POST['video_url']
        instream_ads = self.request.POST['instream']
        discovery_ads = self.request.POST['discovery']  

        # recaptcha_response = request.POST['g-recaptcha-response']

        # url = 'https://www.google.com/recaptcha/api/siteverify'
        # payload = {
        #     'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
        #     'response': recaptcha_response
        # }
        # data = urllib.parse.urlencode(payload).encode()
        # req = urllib.request.Request(url, data=data)
        # response = urllib.request.urlopen(req)
        # result = json.loads(response.read().decode())

        # if (not result['success']) or (not result['action'] == 'create'):
        #     return HttpResponse("error-captcha")
        
        blocked = models.block_channels.objects.filter(block_channels=video_url)
        if blocked:
            return HttpResponse("error-blocklist")

        whitelisted = models.whitelist_channels.objects.filter(whitelist_channels=video_url)
        if whitelisted:
            pass
        else:
            return HttpResponse("error-whitelist")

        if keywords != '':
            keyword = keywords.split(',')
            for i in keyword:
                k = models.banned_keywords.objects.filter(banned_keywords=i)
                if k:
                    return HttpResponse("error-keywords")
        
        ads_format = ''

        if instream_ads == 1:
            ads_format = 'instream_ads'
        else:
            ads_format = 'discovery_ads'

        if model_id is not None:
            m = models.ads_model.objects.get(model_id=model_id)
            m.created_by = user
            m.ad_group_name = ad_name
            m.demographics = 'All'
            m.audiences = 'All'
            m.keywords = keywords
            m.topics = 'All'
            m.placements = 'All'
            m.cpv_bid = cpv_bid
            m.url = video_url
            m.ads_format = ads_format
            m.approved=0
            m.pause=0
            m.update_pending = 1
            m.save()
        else:
            m = models.ads_model.objects.create(
                created_by = user,
                ad_group_name = ad_name,
                demographics = 'All',
                audiences = 'All',
                keywords = keywords,
                topics = 'All',
                placements = 'All',
                cpv_bid = cpv_bid,
                url = video_url,
                ads_format = ads_format
            )
            m.save()
            models.ads_report.objects.create(link=m)
        return HttpResponse("Your Applicaiton submitted")

