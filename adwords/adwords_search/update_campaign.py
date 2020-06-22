import argparse
import sys

import google.ads.google_ads.errors
import google.ads.google_ads.client
from google.api_core import protobuf_helpers
from adwords.get_client import get_client
from adwords.get_campaign import get_campaign
from adwords import models
import datetime

_DATE_FORMAT = '%Y%m%d'

def update_campaign(data):
    client = get_client()
    customer_id = '5397526643'
    m = models.campaign.objects.get(model_id=data)
    campaign_id = m.campaign_id

    campaign_service = client.get_service('CampaignService', version='v3')
    campaign_operation = client.get_type('CampaignOperation', version='v3')
    campaign = campaign_operation.update
    campaign.resource_name = campaign_service.campaign_path(
        customer_id, campaign_id)
    campaign.status = client.get_type('CampaignStatusEnum', version='v3').ENABLED
    campaign.network_settings.target_search_network.value = False

    start_time = datetime.date.today() + datetime.timedelta(days=1)
    campaign.start_date.value = datetime.date.strftime(start_time,
                                                       _DATE_FORMAT)

    if m.end_date != datetime.date.today() + datetime.timedelta(days=1):
        end_time = m.end_date
        campaign.end_date.value = datetime.date.strftime(end_time, _DATE_FORMAT)
    else:
        end_time = start_time + datetime.timedelta(weeks=4)
        campaign.end_date.value = datetime.date.strftime(end_time, _DATE_FORMAT)

    # Retrieve a FieldMask for the fields configured in the campaign.
    fm = protobuf_helpers.field_mask(None, campaign)
    campaign_operation.update_mask.CopyFrom(fm)

    try:
        campaign_response = campaign_service.mutate_campaigns(
            customer_id, [campaign_operation])
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)


    ad_group_id = m.ad_group_id
    ad_group_service = client.get_service('AdGroupService', version='v3')
    ad_group_operation = client.get_type('AdGroupOperation', version='v3')
    ad_group = ad_group_operation.update
    ad_group.resource_name = ad_group_service.ad_group_path(customer_id, ad_group_id)
    ad_group.status = client.get_type('AdGroupStatusEnum', version='v3').ENABLED

    # do the field updation here

    fm = protobuf_helpers.field_mask(None, ad_group)
    ad_group_operation.update_mask.CopyFrom(fm)

    try:
        ad_group_response = ad_group_service.mutate_ad_groups(
            customer_id, [ad_group_operation])
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    m.update_pending = 0
    m.pause = 0
    m.approved = 1
    m.save()
    if m.keywords is not None:
        return add_keywords(client, customer_id, a[3], campaign_details.keywords)
    else:
        return None