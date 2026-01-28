from django.db import models

class Professional(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Nome completo / Social")
    occupation = models.CharField(max_length=100,    verbose_name="Profissão")
    address = models.TextField(verbose_name="Endereço")
    contact = models.CharField(max_length=100, verbose_name="Contato (Email/telefone)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} -{self.occupation}"


class Appointment(models.Model):
    professional = models.ForeignKey(
            Professional,
            on_delete=models.CASCADE,
            related_name='appointments',
            verbose_name="Profissional"
    )

    date = models.DateTimeField(verbose_name="Data e hora da consulta")

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Consulta com {self.professional.full_name} em {self.date}"

