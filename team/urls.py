from django.urls import path
from . import views

app_name = 'team'

urlpatterns = [
    path('', views.ProfissionalView.as_view(), name='profissional-view'),
    path('create/', views.ProfissionalCreateView.as_view(), name='profissional-create'),
    path('update/<uuid:pk>/', views.ProfissionalUpdateView.as_view(), name='profissional-update'),
    path('delete/<uuid:pk>/', views.ProfissionalDeleteView.as_view(), name='profissional-delete'),
]

