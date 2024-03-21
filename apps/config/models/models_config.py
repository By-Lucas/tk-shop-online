from django.db import models

from helpers.utils import image_path
from helpers.base_models import BaseModelTimestamp


class ConfigModel(BaseModelTimestamp):
    offer_group = models.URLField(max_length=2500, verbose_name='URL grupo de ofertas principal', null=True, blank=True)
    time_hours_product = models.IntegerField(verbose_name='Tempo para deletar cada produto', default=72)
    image = models.FileField(verbose_name="Logo", max_length=250, null=True, blank=True, upload_to=image_path)
    image_aba = models.FileField(verbose_name="Imagem da aba", max_length=250, null=True, blank=True, upload_to=image_path)
    send_product_group = models.BooleanField(verbose_name="Enviar produto para os grupos?", null=True, blank=True, default=False,
                                             help_text="Ao salvar deseja enviar os produtos para os grupos do whtsapp e telegram?")
    send_product_description = models.TextField(verbose_name='Descrição para envio da mensagem', null=True, blank=True, 
                                               default="""✅{titulo}✅
                                               \n\n🔥 R${preco}
                                               \n🔖 Use o cupom: {cupom}
                                               \n🛍 Compre aqui: {link_produto}
                                               \n\n😄 Convide seus amigos e familiares para participarem dos nossos grupos de promoção: {link_do_grupo}
                                               \n⚠O link da foto na promo, Não está Clicável ? É só adicionar um dos ADMS em seus contatos""",
                                               help_text="Alem das informações princioais, digite aqui outra informação que deseja enviar: Use o modelo descrito como base")
    
    def __str__(self):
        return "Configuração" if "Configuração" else (self.id)
    
    class Meta:
        verbose_name = "Configurações da empresa"
        verbose_name_plural = "Configurações das empresas"
    
