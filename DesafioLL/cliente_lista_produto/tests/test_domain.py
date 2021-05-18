from uuid import UUID, uuid4

from cliente_lista_produto import domain
from cliente_lista_produto.models import Client
from cliente_lista_produto.integracao.base import BaseApiProduct
import pytest


@pytest.fixture
def data_client():
    return {"name": "user_test", "email": "test@teste.com"}

@pytest.fixture
def client_joaozinho():
    return domain.register_client({"name": "Joãozinho", "email": "joaozinho@teste.com"})

@pytest.fixture
def client_mariazinha():
    return domain.register_client({"name": "Mariazinha", "email": "mariazinha@teste.com"})

class MockProductApi(BaseApiProduct):

    def __init__(self, exist_product: bool):
        self.mock_exist_product = exist_product

    def get_all_product(self, list_product: list) -> list:
        pass

    def get_product(self, id_product: str) -> dict:
        pass

    def exist_product(self, id_product) -> bool:
        return self.mock_exist_product


@pytest.mark.django_db
def test_deve_recuperar_os_dados_do_cliente_quando_o_cliente_existe(client_joaozinho, client_mariazinha):

    clients = domain.view_all_client()

    assert len(clients) == 2
    assert clients[0].name == client_joaozinho.name
    assert clients[1].name == client_mariazinha.name


@pytest.mark.django_db
def test_deve_recuperar_todos_os_clientes_cadastrados(client_joaozinho):
    id_client = client_joaozinho.id
    client = domain.view_client(id_client)

    assert isinstance(client.id, UUID)
    assert client.name == client_joaozinho.name
    assert client.email == client_joaozinho.email

@pytest.mark.django_db
def test_deve_permitir_o_cadastro_do_cliente_quando_os_parametros_estao_corretos(data_client):
    client = domain.register_client(data_client)

    assert isinstance(client.id, UUID)
    assert client.name == data_client["name"]
    assert client.email == data_client["email"]


@pytest.mark.django_db
def test_nao_deve_deixar_cadastrar_um_cliente_com_mesmo_endereco_de_email(data_client):
    with pytest.raises(domain.ClientDuplicate):
        domain.register_client(data_client)
        domain.register_client(data_client)


@pytest.mark.django_db
def test_deve_permitir_alterar_o_email_do_cliente_se_nenhum_cliente_possui_esse_email(client_joaozinho):
    id_client = client_joaozinho.id
    new_data = {"name": "Joãozinho", "email": "teste@teste.com"}
    client = domain.change_client(id_client, new_data)

    assert client.id == id_client
    assert client.email == new_data["email"]
    assert client.name == new_data["name"]


@pytest.mark.django_db
def test_nao_deve_permitir_alterar_o_email_do_cliente_se_um_cliente_ja_possui_esse_email(client_joaozinho):
    with pytest.raises(domain.ClientDuplicate):
        new_client = {"name": "Mariazinha", "email": "mariazinha@teste.com"}
        mariazinha = domain.register_client(new_client)

        id_client = mariazinha.id
        new_data = {"name": "Mariazinha", "email": "joaozinho@teste.com"}
        domain.change_client(id_client, new_data)


@pytest.mark.django_db
def test_deve_permitir_remover_um_cliente_se_um_cliente_esta_cadastrado(client_joaozinho):
    id_client = client_joaozinho.id
    domain.remove_client(id_client)

    client = Client.objects.filter(id=id_client)

    assert len(client) == 0


@pytest.mark.django_db
def test_nao_deve_permitir_remover_um_cliente_se_um_cliente_nao_esta_cadastrado():
    with pytest.raises(domain.ClientNotExist):
        # Id cliente não existente
        id_client = uuid4()
        domain.remove_client(id_client)


@pytest.mark.django_db
def test_deve_permitir_dicionar_um_produto_a_lista_de_favorito_de_um_cliente_quando_o_produto_existe(client_joaozinho):
    # Variavel ára sinalizar o mock que o produto deve existir
    mock_produto_existe = True
    fake_product_api = MockProductApi(mock_produto_existe)
    id_client = str(client_joaozinho.id)
    # ID produto randomico
    id_product = str(uuid4())
    product = domain.add_product_to_list_favorite_client(
        id_product=id_product,
        id_client=id_client,
        product_api=fake_product_api)

    assert product.id_product == id_product
    assert str(product.id_client.id) == id_client


@pytest.mark.django_db
def test_nao_permitir_dicionar_um_produto_a_lista_de_favorito_de_um_cliente_quando_o_produto_nao_existe(client_joaozinho):
    with pytest.raises(domain.ProductNotExist):
        # Variavel ára sinalizar o mock que o produto deve existir
        mock_produto_existe = False
        fake_product_api = MockProductApi(mock_produto_existe)
        id_client = str(client_joaozinho.id)
        # ID produto randomico
        id_product = str(uuid4())
        domain.add_product_to_list_favorite_client(
            id_product=id_product,
            id_client=id_client,
            product_api=fake_product_api)


@pytest.mark.django_db
def test_nao_permitir_dicionar_um_produto_a_lista_de_favorito_de_um_cliente_quando_o_cliente_nao_existe():
    with pytest.raises(domain.ClientNotExist):
        # Variavel para sinalizar o mock que o produto deve existir
        mock_produto_existe = True
        fake_product_api = MockProductApi(mock_produto_existe)
        # id_client randomico (não existe)
        id_client = str(uuid4())
        # id_product randomico (não existe)
        id_product = str(uuid4())
        domain.add_product_to_list_favorite_client(
            id_product=id_product,
            id_client=id_client,
            product_api=fake_product_api)

@pytest.mark.django_db
def test_deve_permitir_remover_um_produto_a_lista_de_favorito_de_um_cliente_quando_o_produto_existe_em_sua_lista(client_joaozinho):
    # Variavel ára sinalizar o mock que o produto deve existir
    mock_produto_existe = True
    fake_product_api = MockProductApi(mock_produto_existe)
    id_client = str(client_joaozinho.id)
    # ID produto randomico
    id_product = str(uuid4())
    product = domain.add_product_to_list_favorite_client(
        id_product=id_product,
        id_client=id_client,
        product_api=fake_product_api)

    domain.remove_product_favorite(id_product=id_product, id_client=id_client)

    products = domain.view_product_favorite(id_client=id_client, product_api=fake_product_api)

    assert len(products) == 0

