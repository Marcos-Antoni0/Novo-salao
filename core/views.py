from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import date
import json

from schedule.models import Schedule


@login_required
def home(request):
    today = date.today()
    
    servicos_do_dia = Schedule.objects.filter(date_schedule=today).count()
    
    pendentes = Schedule.objects.filter(
        date_schedule=today,
        status__in=['agendado', 'em_atendimento']
    ).count()
    
    finalizados = Schedule.objects.filter(
        date_schedule=today,
        status='concluido'
    ).count()
    
    vendas_hoje = Schedule.objects.filter(
        date_schedule=today,
        status='concluido'
    ).aggregate(
        total=Sum('service__price')
    )['total'] or 0
    
    context = {
        'servicos_do_dia': servicos_do_dia,
        'pendentes': pendentes,
        'finalizados': finalizados,
        'vendas_hoje': vendas_hoje,
        'today': today,
    }
    
    return render(request, 'core/home.html', context)


def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Nome de usuário ou senha incorretos"
        else:
            resp['msg'] = "Nome de usuário ou senha incorretos"
    return HttpResponse(json.dumps(resp),content_type='application/json')


# Logout
def logoutuser(request):
    logout(request)
    return redirect('/')