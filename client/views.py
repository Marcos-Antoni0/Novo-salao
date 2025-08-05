from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db.models import Q

from .models import Client
from .forms import ClientForm


@method_decorator(login_required(login_url='login'), name='dispatch')
class ClientView(ListView):
    model = Client
    template_name = 'client/client.html'
    context_object_name = 'clients'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        
        search = self.request.GET.get('search', '').strip()
        if search:
            # Cache da busca por 5 minutos
            cache_key = f'client_search_{hash(search)}_{self.request.user.id}'
            cached_result = cache.get(cache_key)
            
            if cached_result is None:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(email__icontains=search) |
                    Q(phone_number__icontains=search)
                )
                if queryset.count() <= 100:
                    cache.set(cache_key, list(queryset.values_list('id', flat=True)), 300)  # 5 minutos
            else:
                queryset = queryset.filter(id__in=cached_result)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', '')
        context['search'] = search
        
        # Cache do total de clientes
        if not search:
            total_key = f'total_clients_{self.request.user.id}'
            total_clients = cache.get(total_key)
            if total_clients is None:
                total_clients = self.get_queryset().count()
                cache.set(total_key, total_clients, 600)  # 10 minutos
        else:
            total_clients = self.get_queryset().count()
            
        context['total_clients'] = total_clients
        
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_create.html'
    success_url = '/client/'

    def form_valid(self, form):
        cache.delete(f'total_clients_{self.request.user.id}')
        return super().form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_update.html'
    success_url = '/client/'

    def form_valid(self, form):
        cache.delete_many([
            f'total_clients_{self.request.user.id}',
        ])
        return super().form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'client/client_delete.html'
    success_url = '/client/'

    def delete(self, request, *args, **kwargs):
        cache.delete(f'total_clients_{self.request.user.id}')
        return super().delete(request, *args, **kwargs)
