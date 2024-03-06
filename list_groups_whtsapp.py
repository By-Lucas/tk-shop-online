import json
import time
import codecs
import requests
import configparser
from decouple import config


# config = configparser.ConfigParser()
# with codecs.open('config.ini', 'r', encoding='utf-8-sig') as f:
#     config.read_file(f)
    

token__ = 'dqtpfd7vdytwkllk'
insistance__ = 'instance80349'

def all_groups():
    url = f"https://api.ultramsg.com/{insistance__}/groups"
    querystring = {"token": token__}
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 200:
        groups_data = []
        for group in response.json():
            groups_data.append({"name": group["name"], "id": group["id"]})
            print(f'Nome grupo: {group["name"]}  |  ID grupo: {group["id"]}')

        # Salvar os grupos em um arquivo JSON
        with open('grupos.json', 'w', encoding="utf-8") as json_file:
            json.dump(groups_data, json_file, indent=2, ensure_ascii=False)

    else:
        print(f'Ocorreu o seguinte erro ao enviar mensagem para o grupo do whatsapp: {response.text}')

    time.sleep(800)


if __name__ == "__main__":
    all_groups()
    time.sleep(800)
