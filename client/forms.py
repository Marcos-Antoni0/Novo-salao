from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone_number', 'date_birth', 'observations']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Digite o nome completo',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'exemplo@email.com',
                'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': '(11) 99999-9999',
                'class': 'form-control'
            }),
            'date_birth': forms.DateInput(attrs={
                'type': 'date',
                'placeholder': 'dd/mm/aaaa',
                'class': 'form-control date-input',
                'data-toggle': 'datepicker'
            }),
            'observations': forms.Textarea(attrs={
                'placeholder': 'Observações adicionais sobre o cliente...',
                'class': 'form-control',
                'rows': 3
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].required = True
        self.fields['email'].required = False
        self.fields['phone_number'].required = True
        self.fields['date_birth'].required = False
        self.fields['observations'].required = False
        
        # Formatação da data de nascimento se existir uma instância
        if self.instance and self.instance.date_birth:
            self.fields['date_birth'].initial = self.instance.date_birth.strftime('%Y-%m-%d')

    def clean_date_birth(self):
        date_birth = self.cleaned_data.get('date_birth')
        if date_birth:
            if date_birth > date.today():
                raise ValidationError('A data de nascimento não pode ser no futuro.')
            
            today = date.today()
            age = today.year - date_birth.year - ((today.month, today.day) < (date_birth.month, date_birth.day))
            if age < 16:
                 raise ValidationError('Cliente deve ter pelo menos 16 anos.')
            
        return date_birth

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            phone_digits = ''.join(filter(str.isdigit, phone))
            if len(phone_digits) < 10 or len(phone_digits) > 11:
                raise ValidationError('Número de telefone deve ter entre 10 e 11 dígitos.')
        return phone