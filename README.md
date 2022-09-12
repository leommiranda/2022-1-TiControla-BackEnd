## Como levantar a API.

```
# esteja na pasta "2022-1-TiControla/django-api"
cd 2022-1-TiControla-BackEnd/api

# rode o container
sudo docker-compose up --build
```

## Como fazer requisições HTTP para a API usando cURL.
A biblioteca cURL não é necessária. Para converter um comando cURL para uma linguagem de programação (como javascript), use o site <https://curlconverter.com/#javascript>. Para fins de debugging, além do cURL, por exemplo, existem as ferramentas httpie e postman.


##### Como cadastrar um usuário. Observação: é impossível criar um superusuário por meio da API pública.

```
curl -H "Content-Type: application/json" -X POST --data '{"email":"email@gmail.com", "password":"pass"}' "localhost:8000/register/"
```

##### Como fazer o login de um usuário. Atenção: como a nossa autenticação é baseada em sessões de uso, é necessário reutilizar dois outputs gerados pelo login a fim de acessar os dados do usuário. Esses outputs são o "csrftoken" e o "sessionid".

```
curl -H "Content-Type: application/json" -X POST --data '{"email":"email@gmail.com", "password":"pass"}' "localhost:8000/login/"
```

##### Como fazer o logout do usuário. Lembre de reutilizar o "csrftoken" e o "sessionid".

```
curl -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" -X POST 'localhost:8000/logout/'
```

##### Como requisitar dados pessoais do usuário logado (email, nome completo, data de criação do usuário). Essa requisição pode ser usada para mostrar uma tela com os dados pessoais que o usuário informou à API. Lembre de reutilizar o "sessionid".

```
curl -H "Cookie: sessionid=SUBSTITUIR_POR_SESSIONID;" -X GET 'localhost:8000/profile/'
```

##### Como atualizar o nome de um usuário logado. Observação: não é possível atualizar o email. Lembre de reutilizar o "csrftoken" e o "sessionid".

```
curl -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" -X PATCH --data 'full_name=Leonardo Miranda' 'localhost:8000/profile/'
```

##### Como requisitar dados do usuário logado relacionados a finanças. Essa requisição pode ser usada para mostrar o saldo do usuário, o limite disponível do cartão e o limite máximo do cartão. Para cada usuário, só há um valor de saldo, um único valor de limite disponível e um único valor de limite máximo. Lembre de reutilizar o "sessionid".

```
curl -H "Cookie: sessionid=SUBSTITUIR_POR_SESSIONID;" -X GET 'localhost:8000/profile/data/'
```

##### Como atualizar dados do usuário logado relacionados a finanças. Essa requisição pode ser usada para atualizar o saldo do usuário, o limite disponível do cartão e o limite máximo do cartão. Lembre de reutilizar o "csrftoken" e o "sessionid".

```
curl -H "Cookie: csrftoken=SUBSTITUIR_POR_CSRFTOKEN;sessionid=SUBSTITUIR_POR_SESSIONID;" -H "X-CSRFToken: SUBSTITUIR_POR_CSRFTOKEN" -X PATCH --data 'limite_maximo=7000&limite_disponivel=1500' 'localhost:8000/profile/data/'
```


## Como gerar migrations

```
# baixe a imagem docker a partir do Docker Hub
docker pull leommiranda/ti-controla-django-api

# navegue até o diretório "src"
cd src

# rode um terminal dentro da imagem docker usando o seguinte comando
docker run --rm -it -v $(pwd):/current_dir -w /current_dir --user "$(id -u):$(id -g)" leommiranda/ti-controla-django-api bash

# crie as migrations
python3 manage.py makemigrations
python3 manage.py makemigrations user
python3 manage.py makemigrations user_data
```
