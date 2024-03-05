from django.utils.translation import gettext_lazy as _


# TIPO DE USUARIOS
TYPE_USER_ADMIN = 'admin'
TYPE_USER_COMMON = 'comun'
TYPE_USER_AGENT = 'agent'

USER_TYPE = (
    (TYPE_USER_ADMIN, _('Administrador')),
    (TYPE_USER_COMMON, _('Comun')),
    (TYPE_USER_AGENT, _('Agente')),
)
