from django.shortcuts import render, HttpResponse, redirect
import argparse
from .get_client import get_client, adwords_client
from google_auth_oauthlib.flow import InstalledAppFlow
import argparse
import datetime
import sys
import google.ads.google_ads.client
from adwords import models
import os
import datetime
from adwords.authenticate import authenticate
from adwords.update_campaign import update_campaign
import uuid
from googleads import adwords
import google.ads.google_ads.errors
import google.ads.google_ads.client
from adwords import models
from google.api_core import protobuf_helpers
from adwords.add_keywords import add_keywords
_DATE_FORMAT = '%Y%m%d'

def create_camp(data):
    client = get_client()
    customer_id = "5397526643"
    campaign_details = models.campaign.objects.get(pk=data)
    campaign_budget_service = client.get_service('CampaignBudgetService',
                                                 version='v3')
    campaign_service = client.get_service('CampaignService', version='v3')

    # Create a budget, which can be shared by multiple campaigns.
    campaign_budget_operation = client.get_type('CampaignBudgetOperation',
                                                version='v3')
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name.value = '{} {}'.format(campaign_details.campaigns_name, uuid.uuid4())
    campaign_budget.delivery_method = client.get_type(
        'BudgetDeliveryMethodEnum').STANDARD
    campaign_budget.amount_micros.value = 500000
    # Add budget.
    try:
        campaign_budget_response = (
            campaign_budget_service.mutate_campaign_budgets(
                customer_id, [campaign_budget_operation]))
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    # Create campaign.
    campaign_operation = client.get_type('CampaignOperation', version='v3')
    campaign = campaign_operation.create
    campaign.name.value = '{} {}'.format(campaign_details.campaigns_name, uuid.uuid4())
    campaign.advertising_channel_type = client.get_type(
        'AdvertisingChannelTypeEnum').SEARCH
    campaign.status = client.get_type('CampaignStatusEnum', version='v3').ENABLED
    # Set the bidding strategy and budget.
    campaign.manual_cpc.enhanced_cpc_enabled.value = True
    campaign.campaign_budget.value = (
        campaign_budget_response.results[0].resource_name)

    # Set the campaign network options.
    campaign.network_settings.target_google_search.value = True
    campaign.network_settings.target_search_network.value = True
    campaign.network_settings.target_content_network.value = False
    campaign.network_settings.target_partner_search_network.value = False

    # Optional: Set the start date.
    start_time = datetime.date.today() + datetime.timedelta(days=1)
    campaign.start_date.value = datetime.date.strftime(start_time,
                                                       _DATE_FORMAT)

    # Optional: Set the end date.
    if campaign_details.end_date != datetime.date.today() + datetime.timedelta(days=1):
        end_time = campaign_details.end_date
        campaign.end_date.value = datetime.date.strftime(end_time, _DATE_FORMAT)
    else:
        end_time = start_time + datetime.timedelta(weeks=4)
        campaign.end_date.value = datetime.date.strftime(end_time, _DATE_FORMAT)

    # Add the campaign.
    campaign_id = ''
    try:
        campaign_response = campaign_service.mutate_campaigns(
            customer_id, [campaign_operation])        
        cap = campaign_response.results[0].resource_name
        c = cap.split('/')
        campaign_id = c[3]
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
    
    # client = adwords_client()
    ad_group_service = client.get_service('AdGroupService', version='v3')
    campaign_service = client.get_service('CampaignService', version='v3')

    # Create ad group.
    ad_group_operation = client.get_type('AdGroupOperation', version='v3')
    ad_group = ad_group_operation.create
    ad_group.name.value = '{} {}'.format(campaign_details.ad_group_name, uuid.uuid4())
    ad_group.status = client.get_type('AdGroupStatusEnum', version='v3').ENABLED
    ad_group.campaign.value = campaign_service.campaign_path(
        customer_id, campaign_id)
    ad_group.type = client.get_type('AdGroupTypeEnum',
                                    version='v3').SEARCH_STANDARD
    ad_group.cpc_bid_micros.value = 10000000

    # Add the ad group.
    a = []
    try:
        ad_group_response = ad_group_service.mutate_ad_groups(
            customer_id, [ad_group_operation])
        ad = ad_group_response.results[0].resource_name
        a = ad.split('/')
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    print('Created ad group %s.' % ad_group_response.results[0].resource_name)
        
    campaign_details.campaign_id = campaign_id
    campaign_details.ad_group_id = a[3]
    campaign_details.approved = 1
    campaign_details.pause = 0
    campaign_details.save()
    if campaign_details.keywords is not None:
        return add_keywords(client, customer_id, a[3], campaign_details.keywords)
    else:
        return None