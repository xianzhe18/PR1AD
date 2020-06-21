from django.urls import path, re_path
from . import views

app_name = 'adwords'

urlpatterns = [
    # path('edit_campaign/<str:model_id>', views.edit_campaign, name="edit_campaign"),
    path('approve_campaigns/<str:c_id>', views.approve_campaigns, name="approve_campaigns"),
    path('campaign_details/<str:c_id>', views.campaign_details, name="campaign_details"),
    # path('get_token/', views.test_token_view, name="test_token"),
    path('campaign/reports/<str:c_id>', views.reports, name="reports"),
    path('campaign/delete/<str:c_id>', views.delete_campaigns, name="delete_campaign"),
    path('campaign/enable/<str:c_id>', views.enable, name="enable_campaign"),
    path('campaign/pause/<str:c_id>', views.pause_campaigns, name="pause_campaign"),
    path('campaign/edit/<str:c_id>', views.edit_campaigns, name="edit_campaign"),
    path('campaign/create/', views.Create_Campaigns.as_view(), name="create_campaign"),
    path('campaigns/', views.all_campaigns, name="all_campaigns"),
    path('', views.index, name='index'),
]
