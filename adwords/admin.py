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
    model = models.ads_report

@admin.register(models.restriction)
class competition_admin(admin.ModelAdmin):
    inlines = [
        block_channels_Admin,
        whitelist_channels_Admin,
        banned_keywords_Admin,
        ads_percentage_Admin
    ]

@admin.register(models.ads_model)
class ads_model_admin(admin.ModelAdmin):
    inlines = [
        reports_Admin
    ]

