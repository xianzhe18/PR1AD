import argparse
import sys
from adwords import models
from google.api_core import protobuf_helpers
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.util import ResourceName
from adwords.get_client import get_client
import google

def enable_campaign(data):
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
    # Retrieve a FieldMask for the fields configured in the campaign.
    fm = protobuf_helpers.field_mask(None, campaign)
    campaign_operation.update_mask.CopyFrom(fm)

    # Update the campaign.
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

    m.pause = 0
    m.approved = 1
    m.save()
    return None