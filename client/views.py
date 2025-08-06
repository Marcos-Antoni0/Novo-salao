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
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        
        search = self.request.GET.get('search', '').strip()
        if search:
            # Aplicar filtro de busca diretamente no queryset
            # Remover cache complexo que pode estar causando problemas
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone_number__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', '')
        context['search'] = search
        
        # Total de clientes sempre será o total geral (não filtrado)
        total_key = f'total_clients_{self.request.user.id}'
        total_clients = cache.get(total_key)
        if total_clients is None:
            total_clients = Client.objects.count()  # Total geral, não filtrado
            cache.set(total_key, total_clients, 600)  # 10 minutos
            
        context['total_clients'] = total_clients
        
        # Debug: adicionar informações de paginação
        if hasattr(context, 'page_obj'):
            print(f"Página atual: {context['page_obj'].number}")
            print(f"Total de páginas: {context['page_obj'].paginator.num_pages}")
            print(f"Items por página: {self.paginate_by}")
            print(f"Total de items: {context['page_obj'].paginator.count}")
        
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
