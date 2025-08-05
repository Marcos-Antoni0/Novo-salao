from django.db import models
import uuid
from service.models import Category


class Profissional(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Nome")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Telefone")
    especialty = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='profissionais', 
        verbose_name="Especialidade"
    )
    date_contract = models.DateField(verbose_name="Data de contratação")
    ative = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Profissional"
        verbose_name_plural = "Profissionais"
