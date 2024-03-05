from django.db import models

from company.models.models_company import Company
from helpers.base_models import BaseModelTimestamp


class ConfigAds(BaseModelTimestamp):
    name = models.CharField(verbose_name="Nome do anuncio", max_length=200)
    tag_meta_ads = models.TextField(verbose_name="Script Meta do anuncio", max_length=2000, 
                                  help_text='''Modelo do script meta: <meta name="google-adsense-account" content="ca-pub-9679651013955080">''', 
                                  null=True, blank=True)
    script_ads = models.TextField(verbose_name="Script do anuncio", max_length=2000, 
                                  help_text='''Modelo do script: <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6546541654615615151" crossorigin="anonymous"></script>''', 
                                  null=True, blank=True)
    ads_txt = models.FileField(verbose_name="Importar ads.txt",
                                  help_text='''ads.txt é um arquivo txt que o google ads pede para adicionar, um dos formato: google.com, pub-9679651013955080, DIRECT, f08c47fec0942fa5''', 
                                  null=True, blank=True)

    def __str__(self) -> str:
        return self.name if self.name else str(self.id)

    class Meta:
        verbose_name = "Configuração ADS"
        verbose_name_plural = "Configurações ADS"
