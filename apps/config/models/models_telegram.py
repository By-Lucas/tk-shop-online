
from django.db import models

from company.models.models_company import Company
from helpers.base_models import BaseModelTimestamp


class AuthTelegramModel(BaseModelTimestamp):
    company = models.ForeignKey(Company, verbose_name="Empresa", on_delete=models.CASCADE)
    bot_name = models.CharField(verbose_name="Nome do Bot", max_length=100, help_text="Nome do bot Telegram", null=True, blank=True)
    bot_token = models.CharField(verbose_name="Token", max_length=500, help_text="Token do bot Telegram", null=True, blank=True)

    def __str__(self) -> str:
        return self.company.name if self.company.name else str(self.id)

    class Meta:
        verbose_name = "Autenticação Telegram"
        verbose_name_plural = "Autenticação Telegram"


class TelegramGroups(BaseModelTimestamp):
    company = models.ForeignKey(Company, verbose_name="Empresa", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='Nome do grupo telegram', null=True, blank=True)
    group_id = models.CharField(max_length=255, verbose_name='ID do grupo telegram', null=True, blank=True)
    send_msg = models.BooleanField(verbose_name="Enviar menssávem para o grupo?", default=True)
        
    def __str__(self):
        return self.name if self.name else (self.id)
    
    class Meta:
        verbose_name = "Grupo telegram"
        verbose_name_plural = "Grupo telegram"
