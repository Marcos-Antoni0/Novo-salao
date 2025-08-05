from django import forms
from .models import Category, Service


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas categorias ativas
        self.fields['category'].queryset = Category.objects.filter(ative=True)
        
    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category and not category.ative:
            raise forms.ValidationError("Não é possível selecionar uma categoria inativa.")
        return category