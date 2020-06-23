import argparse
import sys
import google.ads.google_ads.errors
from google.api_core import protobuf_helpers
import google.ads.google_ads.client
from adwords import models
from adwords.get_client import get_client

def remove_campaigns(data):
    c = models.campaign.objects.get(model_id=data)
    ads_model = c.ads_model
    client = get_client()
    customer_id = '5397526643'

    campaign_service = client.get_service('CampaignService', version='v3')
    campaign_operation = client.get_type('CampaignOperation', version='v3')

    resource_name = campaign_service.campaign_path(customer_id, ads_model)
    campaign_operation.remove = resource_name

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

    print('Removed campaign %s.' % campaign_response.results[0].resource_name)
    c.delete()
    return None