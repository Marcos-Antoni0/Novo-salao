from django import forms
from django.utils import timezone
from .models import Schedule
from client.models import Client
from team.models import Profissional
from service.models import Service


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['client', 'profissional', 'service', 'status', 'date_schedule', 'time_schedule']
        widgets = {
            'date_schedule': forms.DateInput(attrs={'type': 'date'}),
            'time_schedule': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas registros ativos
        self.fields['client'].queryset = Client.objects.filter(ative=True)
        self.fields['profissional'].queryset = Profissional.objects.filter(ative=True)
        self.fields['service'].queryset = Service.objects.filter(ative=True)
        
    def clean_client(self):
        client = self.cleaned_data.get('client')
        if client and not client.ative:
            raise forms.ValidationError("Não é possível selecionar um cliente inativo.")
        return client
    
    def clean_profissional(self):
        profissional = self.cleaned_data.get('profissional')
        if profissional and not profissional.ative:
            raise forms.ValidationError("Não é possível selecionar um profissional inativo.")
        return profissional
    
    def clean_service(self):
        service = self.cleaned_data.get('service')
        if service and not service.ative:
            raise forms.ValidationError("Não é possível selecionar um serviço inativo.")
        return service
    
    def clean(self):
        cleaned_data = super().clean()
        profissional = cleaned_data.get('profissional')
        service = cleaned_data.get('service')
        
        # Verificar se o profissional pode executar o serviço
        if profissional and service:
            if profissional.especialty != service.category:
                raise forms.ValidationError(
                    f"O profissional {profissional.name} não pode executar serviços da categoria {service.category.name}. "
                    f"Sua especialidade é {profissional.especialty.name}."
                )
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Se o status foi alterado para concluído, definir data de conclusão
        if instance.status == 'concluido' and not instance.data_conclusao:
            instance.data_conclusao = timezone.now()
        # Se o status foi alterado de concluído para outro, remover data de conclusão
        elif instance.status != 'concluido' and instance.data_conclusao:
            instance.data_conclusao = None
            
        if commit:
            instance.save()
        return instance

