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
from adwords.update_campaign import update_campaign
from adwords.create_camp import create_camp
from adwords.pause_campaign import pause_campaign
from adwords.remove_campains import remove_campaigns
from adwords.report_campaign import report_campaign
from adwords.get_campaign import get_campaign
from .enable_campaign import enable_campaign

from django.views.decorators.clickjacking import xframe_options_exempt
import uuid
from googleads import adwords
GOOGLE_RECAPTCHA_SECRET_KEY = 'private-key'

_DATE_FORMAT = '%Y%m%d'
# from .get_campaign import get_campaign
# get_campaign()


def index(request):
    user = request.user.username
    m = models.campaign.objects.filter(created_by=user)
    if m:
        return render(request, 'index.html', {'campaigns': m})
    else:
        return render(request, 'index.html')

def approve_campaigns(request, c_id):
    try:
        m = models.campaign.objects.get(model_id=c_id)
        if m.update_pending == 1:
            update_campaign(c_id)
        else:
            create_camp(c_id)
        return redirect('adwords:all_campaigns')
    except (ObjectDoesNotExist, EOFError):
        error = "Some Unknown Error Occured"
        return render(request, 'campaign_details.html', {'e': error})

@xframe_options_exempt
def campaign_details(request, c_id):
    try:
        campaign_details = models.campaign.objects.get(pk=c_id)
        return render(request, 'campaign_details.html', {'c': campaign_details})
    except ObjectDoesNotExist:
        error = "This Campaign Does Not Exists"
        return render(request, 'campaign_details.html', {'e': error})    

def enable(request, c_id):
    try:
        enable_campaign(c_id)
        return redirect('adwords:index')
    except ObjectDoesNotExist:
        error = "This Campaign Does Not Exists"
        return render(request, 'campaign_details.html', {'e': error})    

def all_campaigns(request):
    m = models.campaign.objects.all()
    if m:
        data = {
            'campaigns': m
        }
        return render(request, 'campaigns.html', data)
    else:
        return render(request, 'campaigns.html')


def reports(request, c_id):
    r = report_campaign(c_id)
    data = {
        'cpm': r.cpm,
        'cpv': r.cpv
    }
    return render(request, 'reports.html', data)

def pause_campaigns(request, c_id):
    pause_campaign(c_id)
    return redirect('adwords:index')

def delete_campaigns(request, c_id):
    remove_campaigns(c_id)
    return redirect('adwords:index')

def edit_campaigns(request, c_id):
    return render(request, 'index.html', {'model': c_id})


class Create_Campaigns(View):
    def post(self, *args, **kwargs):
        user = self.request.user.username
        model_id = self.request.POST['model_id'] or None
        name = self.request.POST['campaign_name']
        strategy = self.request.POST['strategy']
        enddate = self.request.POST['enddate']
        startdate = self.request.POST['startdate']
        budgetdates = self.request.POST['budgetdates']
        search_results = self.request.POST['search_results']
        youtube_videos = self.request.POST['youtube_videos']
        video_partners = self.request.POST['video_partners']
        expanded = self.request.POST['expanded']
        standard = self.request.POST['standard']
        limited = self.request.POST['limited']

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
        inventory_type = ''

        if expanded == 1 :
            inventory_type = 'expanded'
        elif standard == 1 :
            inventory_type = 'standard'
        else:
            inventory_type = 'limited'

        if instream_ads == 1:
            ads_format = 'instream_ads'
        else:
            ads_format = 'discovery_ads'

        if budgetdates == 'Daily':
            startdate = datetime.date.today() + datetime.timedelta(days=30)
            enddate = datetime.date.today() + datetime.timedelta(days=30)

        if model_id is not None:
            m = models.campaign.objects.get(model_id=model_id)
            m.created_by = user
            m.campaigns_name = name
            m.bidding_strategy = strategy
            m.budget_type = budgetdates
            m.start_date = startdate
            m.end_date = enddate
            m.youtube_search_results = search_results
            m.youtube_videos = youtube_videos
            m.video_partners = video_partners
            m.languages = 'All'
            m.locations = 'All'
            m.inventory_types = inventory_type
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
            m = models.campaign.objects.create(
                created_by = user,
                campaigns_name = name,
                bidding_strategy = strategy,
                budget_type = budgetdates,
                start_date = startdate,
                end_date = enddate,
                youtube_search_results = search_results,
                youtube_videos = youtube_videos,
                video_partners = video_partners,
                languages = 'All',
                locations = 'All',
                inventory_types = inventory_type,
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
            models.campaign_reports.objects.create(link=m)
        return HttpResponse("Your Applicaiton submitted")

