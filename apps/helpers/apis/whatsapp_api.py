"""
Documentação da api: https://docs.ultramsg.com/api/post/messages/image
"""
import os
import time
import requests
import threading
from loguru import logger

from helpers.utils import get_remote_file_size
from config.models.models_whatsapp import AuthWhatsappModel


def send_message_media_to_group(token, instance_id, chat_id, media_link, caption):
    url = f"https://api.ultramsg.com/{instance_id}/messages/image"
    if media_link.endswith('.mp4'):
        file_size = get_remote_file_size(media_link)
        if file_size > 16777216:  # 16MB (limite máximo para vídeos)
            logger.warning('O vídeo contém mais de 16MB, enviando como imagem.')
        else:
            url = f"https://api.ultramsg.com/{instance_id}/messages/video"

    payload = f"token={token}&to={chat_id}&image={media_link}&caption={caption}"
    if media_link.endswith('.mp4') and get_remote_file_size(media_link) <= 16777216:
        payload = f"token={token}&to={chat_id}&video={media_link}&caption={caption}"
    
    payload = payload.encode('utf8')
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200 and 'error' not in response.text:
        logger.success(f'Mensagem enviada para o grupo: {chat_id}')
    else:
        logger.error(f'Ocorreu um erro ao enviar mensagem para o grupo {chat_id}: {response.text}')


def send_message_to_group(token, instance_id, chat_id, caption):
    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
    payload = f"token={token}&to={chat_id}&body={caption}&priority=10"
    payload = payload.encode('UTF-8')
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code == 200 and 'error' not in response.text:
        logger.success(f'Mensagem enviada para o grupo: {chat_id}')
        return True
    else:
        logger.error(f'Ocorreu um erro ao enviar mensagem para o grupo {chat_id}: {response.text}')
        return response.json()
        
def send_to_whatsapp_group_batch(list_chat_ids_batch, token, instance_id, caption, media_link=None):
    threads = []
    for chat_id in list_chat_ids_batch:
        #thread = threading.Thread(target=send_message_media_to_group, args=(token, instance_id, chat_id, media_link, caption))
        thread = threading.Thread(target=send_message_to_group, args=(token, instance_id, chat_id, caption))
        threads.append(thread)
        thread.start()

    # Aguardar que todas as threads terminem
    for thread in threads:
        thread.join()

def send_to_whatsapp_group(list_chat_ids: list, caption: str, media_link: str = None) -> bool:
    batch_size = 30
    auth_whatsapp = AuthWhatsappModel.objects.first()
    token = auth_whatsapp.token if auth_whatsapp else os.environ['TOKEN']
    instance_id = auth_whatsapp.insitance_id if auth_whatsapp else os.environ['INSISTANCE_ID']

    for i in range(0, len(list_chat_ids), batch_size):
        list_chat_ids_batch = list_chat_ids[i:i+batch_size]
        send_to_whatsapp_group_batch(list_chat_ids_batch, token, instance_id, caption,  media_link)

    return True


def queue_message_whatsapp() -> list:
    auth_whatsapp = AuthWhatsappModel.objects.first()
    
    list_messages = []
    message_count = {}
    page = 1
    
    token__ = auth_whatsapp.token if auth_whatsapp else os.environ['TOKEN']
    insistance__ = auth_whatsapp.insitance_id if auth_whatsapp else os.environ['INSISTANCE_ID']
    
    # token__ = os.environ['TOKEN']
    # insistance__ = os.environ['INSISTANCE_ID']

    while True:
        url = f"https://api.ultramsg.com/{insistance__}/messages?token={token__}&page={page}&limit=200&status=queue"
        response = requests.get(url)

        if response.status_code == 200:
            response = response.json()
            total_pages = int(response['pages'])
            page += 1

            for message in response['messages']:
                # Usando a 'caption' da mensagem como chave
                caption = message['metadata'].get('caption') if message.get('metadata') else None
                if caption:
                    if caption not in message_count:
                        message_count[caption] = {'count': 1, 'message': message}
                    else:
                        message_count[caption]['count'] += 1
                else:
                    # Tratamento para mensagens sem 'caption'
                    non_caption_key = f"no-caption-{message['id']}"  # Usando ID da mensagem como chave
                    message_count[non_caption_key] = {'count': 1, 'message': message}

            if page > total_pages:
                print("Fim da paginação")
                break

    # Convertendo o dicionário de contagem para lista
    for key, value in message_count.items():
        list_messages.append({'caption': key, 'count': value['count'], 'message': value['message']})

    return list_messages

