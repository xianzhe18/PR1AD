import argparse
import sys
from adwords.get_client import get_client
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def get_campaign():
    client = get_client()
    customer_id = '5397526643'
    ga_service = client.get_service('GoogleAdsService', version='v3')

    query = ('SELECT campaign.id, campaign.name FROM campaign '
             'ORDER BY campaign.id')

    # Issues a search request using streaming.
    response = ga_service.search_stream(customer_id, query=query)
    
    ads_model = ''

    try:
        for batch in response:
            for row in batch.results:
                print(f'Campaign with ID {row.campaign.id.value} and name '
                      f'"{row.campaign.name.value}" was found.')
    except GoogleAdsException as ex:
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn field: {field_path_element.field_name}')
        sys.exit(1)
    return ads_model
    