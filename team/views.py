from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Q

from .models import Profissional
from .forms import ProfissionalForm


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfissionalView(ListView):
    model = Profissional
    template_name = 'team/profissional.html'
    context_object_name = 'profissionais'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        
        search = self.request.GET.get('search', '').strip()
        if search:
            # Cache da busca por 5 minutos
            cache_key = f'profissional_search_{hash(search)}_{self.request.user.id}'
            cached_result = cache.get(cache_key)
            
            if cached_result is None:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(email__icontains=search) |
                    Q(phone_number__icontains=search) |
                    Q(especialty__name__icontains=search)
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
        
        # Cache do total de profissionais
        if not search:
            total_key = f'total_profissionais_{self.request.user.id}'
            total_profissionais = cache.get(total_key)
            if total_profissionais is None:
                total_profissionais = self.get_queryset().count()
                cache.set(total_key, total_profissionais, 600)  # 10 minutos
        else:
            total_profissionais = self.get_queryset().count()
            
        context['total_profissionais'] = total_profissionais
        
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfissionalCreateView(CreateView):
    model = Profissional
    form_class = ProfissionalForm
    template_name = 'team/profissional_create.html'
    success_url = '/team/'

    def form_valid(self, form):
        cache.delete(f'total_profissionais_{self.request.user.id}')
        return super().form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfissionalUpdateView(UpdateView):
    model = Profissional
    form_class = ProfissionalForm
    template_name = 'team/profissional_update.html'
    success_url = '/team/'

    def form_valid(self, form):
        cache.delete_many([
            f'total_profissionais_{self.request.user.id}',
        ])
        return super().form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfissionalDeleteView(DeleteView):
    model = Profissional
    template_name = 'team/profissional_delete.html'
    success_url = '/team/'

    def delete(self, request, *args, **kwargs):
        cache.delete(f'total_profissionais_{self.request.user.id}')
        return super().delete(request, *args, **kwargs)
