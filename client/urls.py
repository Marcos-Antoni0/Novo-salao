from django.urls import path
from . import views

app_name = 'client'

urlpatterns = [
    path('', views.ClientView.as_view(), name='client-view'),
    path('client/create/', views.ClientCreateView.as_view(), name='client-create'),
    path('client/uuid:<uuid:pk>/delete/', views.ClientDeleteView.as_view(), name='client-delete'),
    path('client/uuid:<uuid:pk>/update/', views.ClientUpdateView.as_view(), name='client-update'),
]