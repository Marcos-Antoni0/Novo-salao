from django.db import models
import uuid

class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, verbose_name="Nome completo")
    email = models.EmailField(unique=True, verbose_name="E-mail", null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Telefone")
    date_birth = models.DateField(verbose_name="Data de nascimento", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ative = models.BooleanField(default=True, verbose_name="Ativo")
    observations = models.TextField(blank=True, null=True, verbose_name="Observações")

    def __str__(self):
        return f"{self.name}"