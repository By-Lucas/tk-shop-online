from django import template
from config.models.models_config import ConfigModel


register = template.Library()


#@register.filter
@register.simple_tag(takes_context=True)
def contact_links_dict(context):
    config = ConfigModel.objects.first()
    if config:
        context['whatsapp_group']= config.whatsapp_group,
        context['telegram_channel']= config.telegram_channel,
        context['whatsapp_support']= config.whatsapp_support
        return ""
    else:
        return ""
    
    