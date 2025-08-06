from django.contrib import admin
from client.models import Client
from schedule.models import Schedule
from team.models import Profissional
from service.models import Service

admin.site.register(Client)
admin.site.register(Schedule)
admin.site.register(Profissional)
admin.site.register(Service)