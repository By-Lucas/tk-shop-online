import sys
import time
import json
import base64
import typing
import requests
from loguru import logger


class ApiFactory:
    
    def __init__(self, user:str, password:str, url_login:str="https://api.superacessoinfo.com") -> None:
        self.user = user
        self.password = password
        self.url = url_login
        self.access_token = None
        self.token_expires_at = 0
        
        self._headers = {
            "Accept": "*/*",
            "User-Agent": "Thunder Client (https://www.thunderclient.com)" ,
            "Content-Type": "application/json"
            }
        
        
    def _make_request(self, method: str, endpoint: str, params: typing.Dict = None) -> None:
        self._headers = {
            'authorization': f'Bearer {self.get_token()}',
            'Content-Type': 'application/json'
        }
        if method:
            try:
                response = requests.request(method.upper(), f"{self.url}{endpoint}", params=params, headers=self._headers)
            except Exception as e:
                logger.error(f'Erro de conexão ao fazer {method} request para {endpoint}: {e}')
                raise Exception(f'Erro de conexão ao fazer {method} request para {endpoint}: {e}')
        else:
            ValueError()
        
        if response.status_code >= 200 and response.status_code <= 204:
            return response
        else:
            logger.error(f"Erro ao fazer {method} pedido para {endpoint}: {response.json()} (Erro de codigo {response.status_code})")
            raise Exception(f"Erro ao fazer {method} pedido para {endpoint}: {response.json()} (Erro de codigo {response.status_code})")


    def get_token(self):
        if self.access_token:
            return self.access_token

        print('Criando novo token')
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        payload = {
            "login": self.user,
            "senha": self.password
        }
        response = requests.post(f'{self.url}/apinoticiaprod/v1/login', headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            token_data = json.loads(response.content)
            self.access_token = token_data['token']
            print(self.access_token)
            return self.access_token
        else:
            logger.error(f"Erro ao obter o token. Código de status: {response.status_code}")
            raise Exception(f"Erro ao obter o token. Código de status: {response.status_code}")


# api = ApiFactory('ibitu', 'Nj9087qs', 'https://api.superacessoinfo.com')

# # Parâmetros para a solicitação GET
# params = {
#     'after': 0,
#     'inicio': '2023-08-09',
#     'fim': '2023-09-09'
# }

# # Faz a solicitação GET com os parâmetros
# response = api._make_request('GET', '/apinoticiaprod/v1/noticia/', params=params)
# print(response.text)