from django.db import models
import uuid

class campaign_terms(models.Model):
    terms_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class block_channels(models.Model):
    i_id = models.ForeignKey(campaign_terms, on_delete=models.CASCADE)
    block_channels = models.CharField(max_length=100)

class whitelist_channels(models.Model):
    i_id = models.ForeignKey(campaign_terms, on_delete=models.CASCADE)
    whitelist_channels = models.CharField(max_length=100)

class banned_keywords(models.Model):
    i_id = models.ForeignKey(campaign_terms, on_delete=models.CASCADE)
    banned_keywords = models.CharField(max_length=100)

class ads_percentage(models.Model):
    i_id = models.ForeignKey(campaign_terms, on_delete=models.CASCADE)
    ads_percentage = models.IntegerField()

import datetime
class campaign(models.Model):
    model_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=200)
    campaigns_name = models.CharField(max_length=224)
    bidding_strategy = models.CharField(max_length=224)
    budget_type = models.CharField(max_length=100)
    start_date = models.DateField(default=datetime.date.today() + datetime.timedelta(days=30))
    end_date = models.DateField(default=datetime.date.today() + datetime.timedelta(days=30))
    youtube_search_results = models.IntegerField(default=0)
    youtube_videos = models.IntegerField(default=0)
    video_partners = models.IntegerField(default=0)
    languages = models.CharField(max_length=200)
    locations = models.CharField(max_length=200)
    inventory_types = models.CharField(max_length=200)
    ad_group_name = models.CharField(max_length=200)
    demographics = models.CharField(max_length=200)
    audiences = models.CharField(max_length=200)
    keywords = models.CharField(max_length=1000)
    topics = models.CharField(max_length=1000)
    placements = models.CharField(max_length=1000)
    cpv_bid = models.IntegerField(default=0, null=True)
    url = models.CharField(max_length=1000)
    ads_format = models.CharField(max_length=100)
    approved = models.IntegerField(default=0)
    pause = models.IntegerField(default=0)
    update_pending = models.IntegerField(default=0)

    def __str__(self):
        return self.campaigns_name

class campaign_reports(models.Model):
    link = models.OneToOneField(campaign, primary_key=True, on_delete=models.CASCADE)
    cpm = models.IntegerField(default=0)
    cpv = models.IntegerField(default=0)

# campaigns show krwaoo or approved ka button ek def banaoo htpps repsone k sath
# or dashbaord pe user ka banaya huaa campaigns deikhega or uska status or create button

