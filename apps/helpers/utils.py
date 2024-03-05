import os
import ssl
import uuid
import unicodedata
import urllib.request
from loguru import logger
from itertools import islice

from django.conf import settings
from django.utils import timezone
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator


def image_path(instance, filename):
    unique_filename = f"company/{uuid.uuid4()}-{filename}"
    return unique_filename

def image_company_path(instance, filename):
    unique_filename = f"company/{instance.name}/{uuid.uuid4()}-{filename}"
    return unique_filename

def delete_products(products, hours):
    """Deletar produtos que tenhao 48 horas a mais"""
    if products and hours > 0:
        products = products.filter(created_date__lte=timezone.now() - timezone.timedelta(hours=hours))
        # Delete all products
        for product in products:
            product.delete()
        return True

def get_formatted_description(description:str, offer_group, instance):
    product_url = f'{domain_company()}{instance.get_absolute_url()}'
    return description.format(
                titulo=instance.name,
                link_produto=product_url,
                preco=instance.price,
                cupom=instance.coupon if instance.coupon else 'NÃO PRECISA',
                link_do_grupo=offer_group
            )

def chunk_it(seq, size):
    """Divide a sequência em pedaços de um tamanho especificado."""
    it = iter(seq)
    return iter(lambda: tuple(islice(it, size)), ())


def domain_company():
    currente_site = settings.CSRF_TRUSTED_ORIGINS[0]
    return currente_site

def schedulling_email_notice(news_list, mail_subject, mail_template, context, request=None, title='charisma clipping'):
    """Enviar todos os dias as 9 da manhã um email com as noticias do dia"""
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    context['domain'] = current_site
    context["title"] = title
    context["message"] = mail_subject
    
    # Filtrar as notícias com o assunto "QuintoAndar"
    filtered_news = [news for news in news_list if "QuintoAndar" in news.subjects]

    # Criar o conteúdo do e-mail com as notícias filtradas
    email_content = ""
    for news in filtered_news:
        email_content += render_to_string(mail_template, {'news': news})
    
    context["email_content"] = email_content

    message = render_to_string(mail_template, context)

    if (isinstance(context['to_email'], str)):
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = context['to_email']
    mail = EmailMessage(title, message, from_email, to=to_email)
    mail.content_subtype = "html"
    mail.send()


def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()

def send_notification(title:str, message_subject:str, mail_template, context:dict, request=None):
    """Envia uma notificação por email"""
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        current_site = get_current_site(request)
        context["title"] = title
        context['domain'] = current_site
        context["message"] = message_subject
        message = render_to_string(mail_template, context)

        if (isinstance(context['to_email'], str)):
            to_email = []
            to_email.append(context['to_email'])
        else:
            to_email = context['to_email']
        mail = EmailMessage(title, message, from_email, to=to_email)
        mail.content_subtype = "html"
        mail.send()
    except Exception as e:
        logger.error(f'HOUVE OS SEGUINTE ERRO AO ENVIAR E-MAIL: {e}')

def get_unique_username(value):
    """Criar um usuario unico pegando primeiros dados do email"""
    value = value.lower().split('@')
    username = value[0]
    nfkd = unicodedata.normalize('NFKD', username)
    username = "".join([u for u in nfkd if not unicodedata.combining(u)])
    UserModel = get_user_model()
    n = 1
    while True:
        if UserModel.objects.filter(username=username).exists():
            username = f'{username}{n}'
            n += 1
        else:
            return username

def get_remote_file_size(url):
    try:
        # Desativa a verificação do certificado SSL
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        response = urllib.request.urlopen(url, context=ssl_context)
        file_size = int(response.headers['Content-Length'])
        return file_size
    except Exception as e:
        print(f"Erro ao obter o tamanho do arquivo remoto: {e}")
        return None
