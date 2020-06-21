import argparse
import sys

import google.ads.google_ads.client

def add_keywords(client, customer_id, ad_group_id, keyword):
    ad_group_service = client.get_service('AdGroupService', version='v3')
    ad_group_criterion_service = client.get_service('AdGroupCriterionService',
                                                    version='v3')

    # Create keyword.
    ad_group_criterion_operation = client.get_type('AdGroupCriterionOperation',
                                                   version='v3')
    ad_group_criterion = ad_group_criterion_operation.create
    ad_group_criterion.ad_group.value = ad_group_service.ad_group_path(
        customer_id, ad_group_id)
    ad_group_criterion.status = client.get_type(
        'AdGroupCriterionStatusEnum').ENABLED
    ad_group_criterion.keyword.text.value = keyword
    ad_group_criterion.keyword.match_type = client.get_type(
        'KeywordMatchTypeEnum').EXACT

    # Optional field
    # All fields can be referenced from the protos directly.
    # The protos are located in subdirectories under
    # google/ads/googleads/v0/proto.
    # ad_group_criterion.negative.value = True

    # Optional repeated field
    # final_url = ad_group_criterion.final_urls.add()
    # final_url.value = 'https://www.example.com'

    # Add keyword
    try:
        ad_group_criterion_response = (
            ad_group_criterion_service.mutate_ad_group_criteria(
                customer_id, [ad_group_criterion_operation]))
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    print('Created keyword %s.'
          % ad_group_criterion_response.results[0].resource_name)

    return None