from django.contrib import admin

from config.models.models_config import ConfigModel
from config.models.models_social import SocialMedia
from config.models.models_telegram import AuthTelegramModel, TelegramGroups
from config.models.models_whatsapp import AuthWhatsappModel, WhtasappGroups


admin.site.register(ConfigModel)
admin.site.register(SocialMedia)
admin.site.register(AuthTelegramModel)
admin.site.register(TelegramGroups)
admin.site.register(AuthWhatsappModel)
admin.site.register(WhtasappGroups)

