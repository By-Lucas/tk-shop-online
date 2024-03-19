"""
Documentação da api: https://docs.ultramsg.com/api/post/messages/image
"""
import os
import time
import requests
from loguru import logger

from helpers.utils import get_remote_file_size
from config.models.models_whatsapp import AuthWhatsappModel


def send_to_whatsapp_group(list_chat_id: list, media_link: str, caption: str) -> bool:
    auth_whatsapp = AuthWhatsappModel.objects.first()
    
    status = False
    
    token__ = auth_whatsapp.token if auth_whatsapp else os.environ['TOKEN']
    insistance__ = auth_whatsapp.insitance_id if auth_whatsapp else os.environ['INSISTANCE_ID']
    
    # token__ = os.environ['TOKEN']
    # insistance__ = os.environ['INSISTANCE_ID']

    url = f"https://api.ultramsg.com/{insistance__}/messages/image"
    
    if media_link.endswith('.mp4'):
        # Verificar o tamanho do arquivo de vídeo
        file_size = get_remote_file_size(media_link)
        if file_size > 16777216:  # 16MB (limite máximo para vídeos)
            logger.warning('O vídeo contem mais de 16MB, enviando a imagem.')
            url = f"https://api.ultramsg.com/{insistance__}/messages/image"
        else:
            url = F"https://api.ultramsg.com/{insistance__}/messages/video"
            
    
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    for chat_id in list_chat_id:
        time.sleep(1)
    
        payload = f"token={token__}&to={chat_id}&image={media_link}&caption={caption}"
        if media_link.endswith('.mp4') and get_remote_file_size(media_link):
            file_size = get_remote_file_size(media_link)
            if file_size > 16777216: 
                payload = f"token={token__}&to={chat_id}&image={media_link}&caption={caption}"
            else:
                payload = f"token={token__}&to={chat_id}&video={media_link}&caption={caption}"
        
        payload = payload.encode('utf8')
        response = requests.request("POST", url, data=payload, headers=headers)
        if response.status_code == 200 and not 'error' in response.text:
            logger.success(f'Mensagem enviada para o grupo: {chat_id}')
            status = True
            continue
        
        elif response.status_code == 200 and 'error' in response.text:
            logger.error(f'Ocorreu o seguinte erro ao enviar mensagem para o grupo do whatsapp: {response.text}')
            return response.json()

        else:
            logger.error(f'Ocorreu o seguinte erro ao enviar mensagem para o grupo do whatsapp: {response.text}')
            return response.json()
            
    return status


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



# list_chat_id=["120363023864349230@g.us"] # Pode ser numero do telefone ou ID do grupo -> +5574981199190 | 120363023864349230@g.us
# image = "icon_html.png"
# caption="Imagem de teste para ser enviada"
# send_to_whatsapp_group(list_chat_id, image, caption)
