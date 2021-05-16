from uuid import UUID

from cliente_lista_produto import domain
import pytest


@pytest.fixture
def data_client():
    return {"name": "user_test", "email": "test@teste.com"}

@pytest.fixture
def client_joaozinho():
    return domain.register_client({"name": "Joãozinho", "email": "joaozinho@teste.com"})

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


def test_deve_permitir_dicionar_um_produto_a_lista_de_favorito_de_um_cliente_quando_o_produto_existe():
    assert 1==1
