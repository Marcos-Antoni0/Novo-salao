from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    path('categories/', views.CategoryView.as_view(), name='category-view'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/update/<uuid:pk>/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/delete/<uuid:pk>/', views.CategoryDeleteView.as_view(), name='category-delete'),

    path('services/', views.ServiceView.as_view(), name='service-view'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service-create'),
    path('services/update/uuid:<uuid:pk>/', views.ServiceUpdateView.as_view(), name='service-update'),
    path('services/delete/<uuid:pk>/', views.ServiceDeleteView.as_view(), name='service-delete'),
]