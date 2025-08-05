from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.ScheduleView.as_view(), name='schedule-view'),
    path('create/', views.ScheduleCreateView.as_view(), name='schedule-create'),
    path('update/<uuid:pk>/', views.ScheduleUpdateView.as_view(), name='schedule-update'),
    path('delete/<uuid:pk>/', views.ScheduleDeleteView.as_view(), name='schedule-delete'),
    path('detail/<uuid:pk>/', views.schedule_detail_ajax, name='schedule-detail-ajax'),
]

