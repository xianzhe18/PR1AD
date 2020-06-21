from django.contrib import admin

from . import models

class block_channels_Admin(admin.TabularInline):
    model = models.block_channels

class whitelist_channels_Admin(admin.TabularInline):
    model = models.whitelist_channels

class banned_keywords_Admin(admin.TabularInline):
    model = models.banned_keywords

class ads_percentage_Admin(admin.TabularInline):
    model = models.ads_percentage

class reports_Admin(admin.TabularInline):
    model = models.campaign_reports

@admin.register(models.campaign_terms)
class competition_admin(admin.ModelAdmin):
    inlines = [
        block_channels_Admin,
        whitelist_channels_Admin,
        banned_keywords_Admin,
        ads_percentage_Admin
    ]

@admin.register(models.campaign)
class campaign_admin(admin.ModelAdmin):
    inlines = [
        reports_Admin
    ]

