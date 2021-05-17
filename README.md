# API Produtos favoritos de clientes
> O projeto tem como objetivo prover features para um e-commerce para fazer a gestão de produtos favoritos de seus clientes.


A aplicação permite gerenciar clientes, bem como fornecer aos clientes a gestão de uma lista de produtos favoritos.

## Features
- [x] Cadastro de Clientes
- [x] Adicionar produtos na lista de favoritos 
- [x] Remover produtos da lista de favoritos
- [x] Cadastro de usuário para utilização da API


## Tecnologias

- [**Python:**](https://www.python.org/) Linguagem principal
- [**Django Rest Framework:**](https://www.django-rest-framework.org/) Framework da API
- [**PostgreSql:**](https://www.postgresql.org/) Database Principal
- [**Redis:**](https://redis.io/) Cache para consultas de produtos

## Iniciando a aplicação com Docker

```sh
# Clone este repositório
$ git clone https://github.com/josenunesti/api_cliente_produtos_favoritos.git

# Acesse o diretorio da aplicação
$ cd api_cliente_produtos_favoritos/

# Suba a aplicação por meio do compose-file
$ docker-compose -f docker-compose.prod.yml up -d
```
###### Para facilitar o teste, foi disponibilizado no repositório um .env pronto. =) `Obs.: Em cenários reais, deixar o .env no repositório não é aconselhável.`

### Utilizando a aplicação

Antes de interagir com os principais endpoints da API, primeiro vamos criar um usuário para os testes:

**Passo 1** - Criando usuário de teste para uso da API
```sh
curl --location --request POST 'http://localhost:8082/v1/user/create' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "user_test",
    "password": "user_test",
    "email": "user_test@test.com"
}'
```
Resultado esperado: `Status Code: 201`

**Passo 2** - Obtendo o token do usuário de teste
```sh
curl --location --request POST 'http://localhost:8082/v1/get_token_auth' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "user_test",
    "password": "user_test"
}'
```
Resultado esperado: `Status Code: 200`

Obs.: O token de acesso deverá ser passado no header de todas as requisições da API. Exemplo:
```sh
curl --location --request GET 'http://localhost:8082/v1/client' \
--header 'Authorization: Token fa4060a2666c0605ec35f002a83aa4e2fdf353c4'
```

Com o usuário de teste criado, fique à vontade para interagir com os endpoints da API, consulte a documentação:

- `Swagger:` http://localhost:8082/swagger
- `ReDoc:` http://localhost:8082/redoc

## Preparando o ambiente de desenvolvimento

A seguir iremos preparar nosso ambiente de desenvolvimento, subir as dependências com docker, iniciar a aplicação e executar os testes automatizados. 

Passo 1 - Subir as dependências da aplicação via docker (Postgresql e Redis)
## Preparando o ambiente de desenvolvimento

A seguir iremos preparar nosso ambiente de desenvolvimento, subir as dependências com docker, iniciar a aplicação e executar os testes automatizados. 

**Passo 1** - Subindo as dependências da aplicação via docker (Postgresql e Redis)
```sh
# Execute o compose file
$ docker-compose -f docker-compose.dev.yml up -d
```

**Passo 2** - Iniciando a aplicação na máquina local
```sh
# Acesse o diretorio
$ cd api_cliente_produtos_favoritos/

# Instale o virtualenv
$ pip install virtualenv

# Crie um novo virtualenv
$ virtualenv venv

# (Windows) Ative a venv
$ venv\Scripts\activate

# (Linux ou MacOS) Ative a venv
$ source venv/bin/activate

# Instale as dependências do projeto
$ pip install -r requirements.txt

# Acesse o diretorio
$ cd DesafioLL/

# Execute as migrações para criar a estrutura de banco de dados
$ python manage.py migrate

# Inicie a aplicação
$ python manage.py runserver 0.0.0.0:8082
```

**Passo 3** - Executar os testes automatizados

```sh
# Acesse o diretorio
$ cd api_cliente_produtos_favoritos/
$ cd DesafioLL/

# Execute os testes
$ pytest
```

## Trabalhos futuros
- Adicionar a arquitetura um `load balancing` e `proxy reverso` [(Nginx)](https://www.nginx.com/) para auxiliar a escalabilidade da API.
- Estudar a viabilidade de implementar o pattern [Circuit Breaker](https://martinfowler.com/bliki/CircuitBreaker.html) para aumentar a robustez da aplicação em casos de falha da API externa de produtos.

## Meta

José Humberto – josenunesti@gmail.com

Distribuído sob a licença GNU General Public License v3. Veja `LICENSE` para mais informações.

[https://github.com/josenunesti](https://github.com/josenunesti)