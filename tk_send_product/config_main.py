from django.contrib.messages import constants


LOGIN_URL = "accounts:login"
X_FRAME_OPTIONS = 'SAMEORIGIN'
AUTH_USER_MODEL = 'accounts.User'
IMPORT_EXPORT_USE_TRANSACTIONS = True 

# Quantidade de items para remover pelo django admin
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

JET_SIDE_MENU_COMPACT = True
JET_CHANGE_FORM_SIBLING_LINKS = True

TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.request' )


JET_THEMES = [
    # {
    #     'theme': 'dark',
    #     'color': 'black',
    #     'title': 'Dark',
    # },
    {
        'theme': 'default', # theme folder name
        'color': '#47bac1', # color of the theme's button in user menu
        'title': 'Default' # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#333',
        'title': 'Light Gray'
    }
]

JET_DEFAULT_THEME = 'default'  # Nome do tema padrão


# TAGS MESSAGE TEMPLATE
MESSAGE_TAGS = {
    constants.DEBUG: 'primary',
    constants.ERROR: 'danger',
    constants.SUCCESS: 'success',
    constants.INFO: 'info',
    constants.WARNING: 'warning',
}
