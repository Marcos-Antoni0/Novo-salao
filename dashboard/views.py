from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from datetime import datetime, timedelta
from schedule.models import Schedule
from collections import defaultdict


@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')


@login_required(login_url='login')
def dashboard_data_ajax(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    
    if not start_date or not end_date:
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    schedules = Schedule.objects.filter(
        status='concluido',
        data_conclusao__isnull=False,
        data_conclusao__date__gte=start_date,
        data_conclusao__date__lte=end_date
    ).values('data_conclusao')
    
    date_counts = defaultdict(int)
    
    for schedule in schedules:
        date_key = schedule['data_conclusao'].date()
        date_counts[date_key] += 1

    labels = []
    data = []
    
    current_date = start_date
    
    while current_date <= end_date:
        labels.append(current_date.strftime('%d/%m/%Y'))
        data.append(date_counts.get(current_date, 0))
        current_date += timedelta(days=1)
    
    total_concluidos = sum(data)
    media_diaria = round(total_concluidos / len(data), 1) if data else 0
    
    max_servicos = max(data) if data else 0
    melhor_dia = ''
    
    if max_servicos > 0:
        max_servicos_index = data.index(max_servicos)
        melhor_dia = labels[max_servicos_index]
    
    response_data = {
        'chart_data': {
            'labels': labels,
            'datasets': [{
                'label': 'Serviços Concluídos',
                'data': data,
                'borderColor': 'rgb(75, 192, 192)',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'tension': 0.1,
                'fill': True
            }]
        },
        'stats': {
            'total_concluidos': total_concluidos,
            'media_diaria': media_diaria,
            'melhor_dia': melhor_dia,
            'max_servicos': max_servicos,
            'periodo_dias': len(data)
        }
    }
    
    return JsonResponse(response_data)