import requests


def get_token():
    url = 'http://localhost:8000/conta/api/v1/token/'

    data = {
        "email": "lucasdev@gmail.com",
        "password": "123",
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        token = response.json()['access']
        print('Token:', token)
        return token
    
    else:
        print('Error getting token: {}'.format(response.status_code))


def create_product(data: dict):
    url = 'http://127.0.0.1:8000/produtos/api/v1/products/'

    token = get_token()
    if not token:
        print('Erro na autenticação')
        return

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 201:
        print(response.json())
        print('Product created successfully!')
    else:
        print('Error creating product: {}'.format(response.status_code))


data = {
        "company": 1,
        "name": "Teste",
        "description": "",
        "price": "500.00",
        "category": None,
        "quantity_in_stock": None,
        "affiliate_link": "",
        "featured": False,
        "image": None,
        "created_at": "2023-08-07T23:22:59.681856-03:00",
        "updated_at": "2023-08-07T23:22:59.681856-03:00"
    }

create_product(data)
