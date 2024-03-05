import requests

def queue_message() -> list:
    list_messages = []
    message_count = {}
    page = 1

    while True:
        url = f"https://api.ultramsg.com/instance67010/messages?token=vaix1pn9oaelwhd3&page={page}&limit=200&status=queue"
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

    # Aqui você pode imprimir a lista de mensagens e suas contagens
    for message in list_messages:
        print(message)
        

queue_message()
