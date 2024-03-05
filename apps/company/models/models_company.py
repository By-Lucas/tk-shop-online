import uuid

from django.db import models
from django.utils.text import slugify

from helpers.base_models import BaseModelTimestamp
from django.utils.translation import gettext_lazy as _


def upload_to(instance ,filename):
    return 'company/{name}/{uuid}-{filename}'.format(
        name=slugify(instance.name), uuid=uuid.uuid4(), filename=filename)
    
    
class Company(BaseModelTimestamp):
    name = models.CharField(verbose_name=_("Nome"), max_length=200)
    phone = models.CharField(verbose_name=_("Telefone"), max_length=15)
    email = models.EmailField(verbose_name=_("E-mail"), max_length=200, unique=True)
    cnpj = models.CharField(verbose_name=_("CNPJ"), max_length=18, null=True, blank=True)
    city = models.CharField(verbose_name=_("Cidade"), max_length=80, null=True, blank=True)
    address = models.CharField(verbose_name=_("Endereço"), max_length=200, null=True, blank=True)
    number_house = models.CharField(verbose_name=_("Número da residência"), max_length=4, null=True, blank=True)
    # url_company = models.CharField(verbose_name=_("URL da empresa"), max_length=2000, null=True, blank=True)
    # name_title_company = models.CharField(verbose_name=_("Título da empresa"), max_length=200, null=True, blank=True)
    # image = models.ImageField(verbose_name=_("Imagem da empresa"), upload_to=upload_to, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name if self.name else (self.id)
    
    class Meta:
        verbose_name = _("Empresa")
        verbose_name_plural = _("Empresas")

