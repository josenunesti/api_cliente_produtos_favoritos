# API Produtos favoritos de clientes
> O projeto tem como objetivo prover features para um e-commerce para fazer a gestão de produtos favoritos de seus clientes.

A aplicação permite cadastrar, alterar, remover e visualizar clientes, bem como adicionar ou remover produtos em uam lista de favoritos dos clientes.

## Principais tecnologias utilizadas

- **Django Rest Framework:** Framework da API
- **PostgreSql:** Database Principal
- **Redis:** Cache dos produtos 

## Iniciando a aplicação com Docker
###### Obs.1: Antes de prosseguir, crie um arquivo .env no diretorio raiz da aplicação. Vide ".env_example" 
###### Obs.2: Fara facilitar o teste, foi disponibilizado no repositorio um .env pronto. =)

```sh
git clone https://github.com/josenunesti/api_cliente_produtos_favoritos.git

cd api_cliente_produtos_favoritos/

docker-compose -f docker-compose.prod.yml up -d
```

## Como usar a aplicação

a) Criando usuário de teste para uso da API
```sh
curl --location --request POST 'http://localhost:8082/api/user/create' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "user_test",
    "password": "user_test",
    "email": "user_test@test.com"
}'
```
Resultado esperado: Status Code: 201

b) Obtendo o token do usuário de teste
```sh
curl --location --request POST 'http://localhost:8082/get_token_auth' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "user_test",
    "password": "user_test"
}'
```
Resultado esperado: Status Code: 200

Obs.: O token de acesso deverá ser passado no header de todas as requisições da API. Exemplo:
```sh
curl --location --request GET 'http://localhost:8082/api/client' \
--header 'Authorization: Token fa4060a2666c0605ec35f002a83aa4e2fdf353c4'
```

## Executando o código

a) Subir as dependências da aplicação via docker (Postgresql e redis)
```sh
docker-compose -f docker-compose.dev.yml up -d
```

b) Iniciar a aplicação na maquina local
```sh
cd api_cliente_produtos_favoritos/
CRIAR VIRTUAL ENV E ATIVA-LO
pip install -r requirements.txt
cd DesafioLL/
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8082
```

## Executando os testes automatizados
###### Obs.: Garanta que os passos acima foram realmente exeuctados.

```sh
cd api_cliente_produtos_favoritos/
cd DesafioLL/
pytest
```

## Meta

José Humberto – josenunesti@gmail.com

Distribuído sob a licença XYZ. Veja `LICENSE` para mais informações.

[https://github.com/josenunesti](https://github.com/josenunesti)