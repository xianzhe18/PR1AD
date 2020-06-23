from django.urls import path, re_path
from . import views

app_name = 'adwords'

urlpatterns = [
    path('approve_ads_models/<str:c_id>', views.approve_ads_models, name="approve_ads_models"),
    path('ads_model_details/<str:c_id>', views.ads_model_details, name="ads_model_details"),
    path('ads_model/reports/<str:c_id>', views.reports, name="reports"),
    path('ads_model/delete/<str:c_id>', views.delete_ads_models, name="delete_ads_model"),
    path('ads_model/enable/<str:c_id>', views.enable, name="enable_ads_model"),
    path('ads_model/pause/<str:c_id>', views.pause_ads_models, name="pause_ads_model"),
    path('ads_model/edit/<str:c_id>', views.edit_ads_models, name="edit_ads_model"),
    path('ads_model/create/', views.Create_ads_models.as_view(), name="create_ads_model"),
    path('ads_models/', views.all_ads_models, name="all_ads_models"),
    path('', views.index, name='index'),
]
