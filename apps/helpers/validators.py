import os
from difflib import SequenceMatcher

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def allow_only_words_validator(value):
    """Verificar se contem mais de uma palavra"""
    validate = value.split(" ")
    preposition = ['da', 'dos', 'do', 'de', 'das', 'e']
    for prepo in preposition:
        if prepo in validate:
            validate.remove(prepo)

    if len(validate) < 2:
        raise ValidationError(_('Este campo deve conter mais de uma palavra'))

def allow_only_images_validator(value):
    'Em caso de erro, deixar somente o value em vez de value.name'
    ext = os.path.splitext(value.name)[1]  # cover-image.jpg
    print(ext)
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Tipo de arquivo não suportado. extensões permitidas: ' + str(valid_extensions)))

def allow_only_arquives_validator(value):
    'Em caso de erro, deixar somente o value em vez de value.name'
    ext = os.path.splitext(value.name)[1]  # arquive.pdf
    print(ext)
    valid_extensions = ['.pdf', '.doc', '.docs']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Tipo de arquivo não suportado. extensões permitidas: ' + str(valid_extensions)))

def validator_cpf_or_cnpj(value):
    if not CPF().validate(value):
        if not CNPJ().validate(value):
            raise ValidationError(_('CNPJ ou CPF inválido!'))


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def validate_password_not_similar_to_email(value, email):
    if similar(value, email) > 0.7:  # Ajuste este valor conforme necessário (0 a 1, sendo 1 idêntico)
        raise ValidationError("A senha é muito parecida com o e-mail.")