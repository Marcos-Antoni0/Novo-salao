from django.db import models
import uuid


class Schedule(models.Model): 
    class ScheduleChoice(models.TextChoices):
        AGENDADO = 'agendado', 'Agendado'
        EM_ATENDIMENTO = 'em_atendimento', 'Em atendimento'
        CONCLUIDO = 'concluido', 'Concluído'
        CANCELADO = 'cancelado', 'Cancelado'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE, verbose_name="Cliente")
    profissional = models.ForeignKey('team.Profissional', on_delete=models.CASCADE, verbose_name="Profissional")
    service = models.ForeignKey('service.Service', on_delete=models.CASCADE, verbose_name="Serviço")
    status = models.CharField(max_length=20, choices=ScheduleChoice.choices, default=ScheduleChoice.AGENDADO, verbose_name="Status")
    date_schedule = models.DateField(verbose_name="Data do agendamento")
    time_schedule = models.TimeField(verbose_name="Hora do agendamento")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data_conclusao = models.DateTimeField(null=True, blank=True, verbose_name="Data de conclusão")

    def __str__(self):
        return f"{self.client.name} - {self.date_schedule} {self.time_schedule} - {self.status}"