from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db.models import Q

from .models import Category, Service
from .forms import CategoryForm, ServiceForm

@method_decorator(login_required(login_url='login'), name='dispatch')
class CategoryView(ListView):
    model = Category
    template_name = 'service/category.html'
    context_object_name = 'categories'
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', '')
        context['search'] = search
        context['total_categories'] = self.get_queryset().count()
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'service/category_create.html'
    success_url = '/service/categories/'

    def form_valid(self, form):
        cache.delete(f'total_categories_{self.request.user.id}')
        return super().form_valid(form)
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'service/category_update.html'
    success_url = '/service/categories/'

    def form_valid(self, form):
        cache.delete_many([
            f'total_categories_{self.request.user.id}',
        ])
        return super().form_valid(form)
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'service/category_delete.html'
    success_url = '/service/categories/'

    def delete(self, request, *args, **kwargs):
        cache.delete(f'total_categories_{self.request.user.id}')
        return super().delete(request, *args, **kwargs)


# Service View
@method_decorator(login_required(login_url='login'), name='dispatch')
class ServiceView(ListView):
    model = Service
    template_name = 'service/service.html'
    context_object_name = 'services'
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', '')
        context['search'] = search
        context['total_services'] = self.get_queryset().count()
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service/service_create.html'
    success_url = '/service/services/'

    def form_valid(self, form):
        cache.delete(f'total_services_{self.request.user.id}')
        return super().form_valid(form)
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service/service_update.html'
    success_url = '/service/services/'

    def form_valid(self, form):
        cache.delete_many([
            f'total_services_{self.request.user.id}',
        ])
        return super().form_valid(form)
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'service/service_delete.html'
    success_url = '/service/services/'

    def form_valid(self, form):
        cache.delete(f'total_services_{self.request.user.id}')
        return super().form_valid(form)