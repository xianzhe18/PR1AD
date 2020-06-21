import argparse
import sys

from adwords import models
from adwords.get_client import get_client
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def report_campaign(data):
    client = get_client()
    customer_id = '5397526643'
    
    ga_service = client.get_service('GoogleAdsService', version='v3')

    query = ('SELECT campaign.id, campaign.name, ad_group.id, ad_group.name, '
             'ad_group_criterion.criterion_id, '
             'ad_group_criterion.keyword.text, '
             'ad_group_criterion.keyword.match_type, '
             'metrics.impressions, metrics.clicks, metrics.cost_micros '
             'FROM keyword_view WHERE segments.date DURING LAST_7_DAYS '
             'AND campaign.advertising_channel_type = \'SEARCH\' '
             'AND ad_group.status = \'ENABLED\' '
             'AND ad_group_criterion.status IN (\'ENABLED\', \'PAUSED\') '
             'ORDER BY metrics.impressions DESC '
             'LIMIT 50')

    response = ga_service.search_stream(customer_id, query)
    keyword_match_type_enum = client.get_type(
        'KeywordMatchTypeEnum', version='v2').KeywordMatchType
    m = models.campaign.objects.get(model_id=data)
    r = models.campaign_reports.objects.get(link=m)
    try:
        for batch in response:
            for row in batch.results:
                campaign = row.campaign
                ad_group = row.ad_group
                criterion = row.ad_group_criterion
                metrics = row.metrics
                keyword_match_type = keyword_match_type_enum.Name(
                    criterion.keyword.match_type)
                print(f'Keyword text "{criterion.keyword.text.value}" with '
                      f'match type "{keyword_match_type}" '
                      f'and ID {criterion.criterion_id.value} in '
                      f'ad group "{ad_group.name.value}" '
                      f'with ID "{ad_group.id.value}" '
                      f'in campaign "{campaign.name.value}" '
                      f'with ID {campaign.id.value} '
                      f'had {metrics.impressions.value} impression(s), '
                      f'{metrics.clicks.value} click(s), and '
                      f'{metrics.cost_micros.value} cost (in micros) during '
                      'the last 7 days.')
                if campaign.id.value == m.campaign_id:
                    r.cpm = metrics.impressions.value
                    r.cpv = metrics.clicks.value
                    r.save()
                else:
                    pass
    except GoogleAdsException as ex:
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn field: {field_path_element.field_name}')
        sys.exit(1)
    
    return r