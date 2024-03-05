
from django.db import models

from company.models.models_company import Company
from helpers.base_models import BaseModelTimestamp


class AuthWhatsappModel(BaseModelTimestamp):
    company = models.ForeignKey(Company, verbose_name="Empresa", on_delete=models.CASCADE)
    token = models.CharField(verbose_name="Token", max_length=200, help_text="Token liberado pela plataforma ultramsg", null=True, blank=True)
    insitance_id = models.CharField(verbose_name="Insistance ID", max_length=200, help_text="Insistance ID liberado pela plataforma ultramsg", null=True, blank=True)

    def __str__(self) -> str:
        return self.company.name if self.company.name else str(self.id)

    class Meta:
        verbose_name = "Autenticação Whatsapp"
        verbose_name_plural = "Autenticação Whatsapp"


class WhtasappGroups(BaseModelTimestamp):
    company = models.ForeignKey(Company, verbose_name="Empresa", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='Nome do grupo do whatsapp', null=True, blank=True)
    group_id = models.CharField(max_length=255, verbose_name='ID do grupo do whatsapp', null=True, blank=True)
    send_msg = models.BooleanField(verbose_name="Enviar menssávem para o grupo?", default=True)
    
    def __str__(self):
        return self.name if self.name else (self.id)
    
    class Meta:
        verbose_name = "Grupo whatsapp"
        verbose_name_plural = "Grupo whatsapp"
        