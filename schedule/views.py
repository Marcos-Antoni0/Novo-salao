from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone

from .models import Schedule
from .forms import ScheduleForm


@method_decorator(login_required(login_url='login'), name='dispatch')
class ScheduleView(ListView):
    model = Schedule
    template_name = 'schedule/schedule.html'
    context_object_name = 'schedules'
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'client', 'profissional', 'service', 'service__category'
        ).order_by('-date_schedule', '-time_schedule')
        
        search = self.request.GET.get('search', '').strip()
        status_filter = self.request.GET.get('status', '').strip()
        
        if search:
            queryset = queryset.filter(
                Q(client__name__icontains=search) |
                Q(profissional__name__icontains=search) |
                Q(service__name__icontains=search)
            )
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', '')
        status_filter = self.request.GET.get('status', '')
        
        context['search'] = search
        context['status_filter'] = status_filter
        context['status_choices'] = Schedule.ScheduleChoice.choices
        context['total_schedules'] = self.get_queryset().count()
        
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class ScheduleCreateView(CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'schedule/schedule_create.html'
    success_url = '/schedule/'

    def form_valid(self, form):
        cache.delete(f'total_schedules_{self.request.user.id}')
        return super().form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ScheduleUpdateView(UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'schedule/schedule_update.html'
    success_url = '/schedule/'

    def form_valid(self, form):
        cache.delete_many([
            f'total_schedules_{self.request.user.id}',
        ])
        return super().form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ScheduleDeleteView(DeleteView):
    model = Schedule
    template_name = 'schedule/schedule_delete.html'
    success_url = '/schedule/'

    def delete(self, request, *args, **kwargs):
        cache.delete(f'total_schedules_{self.request.user.id}')
        return super().delete(request, *args, **kwargs)


@login_required(login_url='login')
def schedule_detail_ajax(request, pk):
    """View para retornar detalhes do agendamento via AJAX para o modal"""
    schedule = get_object_or_404(Schedule, pk=pk)
    
    data = {
        'id': str(schedule.id),
        'client_name': schedule.client.name,
        'client_email': schedule.client.email,
        'client_phone': schedule.client.phone_number,
        'profissional_name': schedule.profissional.name,
        'profissional_especialty': schedule.profissional.especialty.name,
        'service_name': schedule.service.name,
        'service_category': schedule.service.category.name,
        'service_price': str(schedule.service.price),
        'service_duration': schedule.service.duration,
        'status': schedule.get_status_display(),
        'status_value': schedule.status,
        'date_schedule': schedule.date_schedule.strftime('%d/%m/%Y'),
        'time_schedule': schedule.time_schedule.strftime('%H:%M'),
        'created_at': schedule.created_at.strftime('%d/%m/%Y %H:%M'),
        'data_conclusao': schedule.data_conclusao.strftime('%d/%m/%Y %H:%M') if schedule.data_conclusao else None,
    }
    
    return JsonResponse(data)
