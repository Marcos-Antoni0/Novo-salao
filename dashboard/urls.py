from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard-view'),
    path('data/', views.dashboard_data_ajax, name='dashboard-data-ajax'),
]

