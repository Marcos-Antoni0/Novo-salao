from django import forms
from .models import Profissional
from service.models import Category


class ProfissionalForm(forms.ModelForm):
    class Meta:
        model = Profissional
        fields = '__all__'
        widgets = {
            'date_contract': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas categorias ativas
        self.fields['especialty'].queryset = Category.objects.filter(ative=True)
        
    def clean_especialty(self):
        especialty = self.cleaned_data.get('especialty')
        if especialty and not especialty.ative:
            raise forms.ValidationError("Não é possível selecionar uma categoria inativa.")
        return especialty

