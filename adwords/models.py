from django.db import models
import uuid

class restriction(models.Model):
    terms_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class block_channels(models.Model):
    i_id = models.ForeignKey(restriction, on_delete=models.CASCADE)
    block_channels = models.CharField(max_length=100)

class whitelist_channels(models.Model):
    i_id = models.ForeignKey(restriction, on_delete=models.CASCADE)
    whitelist_channels = models.CharField(max_length=100)

class banned_keywords(models.Model):
    i_id = models.ForeignKey(restriction, on_delete=models.CASCADE)
    banned_keywords = models.CharField(max_length=100)

class ads_percentage(models.Model):
    i_id = models.ForeignKey(restriction, on_delete=models.CASCADE)
    ads_percentage = models.IntegerField()

import datetime
class ads_model(models.Model):
    model_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=200)
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
        return self.ad_group_name

class ads_report(models.Model):
    link = models.OneToOneField(ads_model, primary_key=True, on_delete=models.CASCADE)
    cpm = models.IntegerField(default=0)
    cpv = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)