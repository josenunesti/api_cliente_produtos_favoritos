from .models import Client, Product
from .integracao.base import BaseApiProduct


def _get_client_by_id(id_client: str) -> Client:
    client = Client.objects.filter(id=id_client)
    if len(client) <= 0:
        return None
    else:
        return client[0]


def _client_registered(email) -> bool:

    client_exist = Client.objects.filter(email=email)
    return len(client_exist) > 0


def register_client(client: dict) -> Client:

    if _client_registered(client["email"]):
        raise ClientDuplicate("Este e-mail já foi utilizado por outro usuário.")

    client = Client(**client)
    client.save()

    return client


def change_client(id_client: str, client_chandeg: dict) -> Client:

    client = _get_client_by_id(id_client)

    if client is None:
        raise ClientNotExist("Cliente não encontrado.")

    if client.email != client_chandeg["email"]:
        if _client_registered(client_chandeg["email"]):
            raise ClientDuplicate("Este e-mail já foi utilizado por outro usuário.")

    client.name = client_chandeg["name"]
    client.email = client_chandeg["email"]
    client.save()

    return client


def view_all_client() -> list:

    return Client.objects.all()


def view_client(id_client: str) -> Client:

    client = _get_client_by_id(id_client)
    if client is None:
        raise ClientNotExist("Cliente não encontrado.")

    return client


def remove_client(id_client: str):

    client = _get_client_by_id(id_client)
    if client is None:
        raise ClientNotExist("Cliente não encontrado.")

    client.delete()


def _get_product_client(id_product: str, id_client: str):
    product = Product.objects.filter(id_product=id_product, id_client=id_client)
    if len(product) <= 0:
        return None
    else:
        return product[0]


def add_product_to_list_favorite_client(id_product: str, id_client: str, product_api: BaseApiProduct) -> Product:

    client = _get_client_by_id(id_client)
    if client is None:
        raise ClientNotExist("Cliente não encontrado.")

    product = _get_product_client(id_product, id_client)
    if product is not None:
        raise ProductExistInList("Esse produto já foi adicionado na lista de favoritos.")

    exist_product = product_api.exist_product(id_product)

    if not exist_product:
        raise ProductNotExist("Produto não encontrado.")

    product = Product(**{"id_product": id_product, "id_client": client})
    product.save()

    return product


def remove_product_favorite(id_product: str, id_client: str):

    client = _get_client_by_id(id_client)
    if client is None:
        raise ClientNotExist("Cliente não encontrado.")

    product = _get_product_client(id_product, id_client)
    if product is None:
        raise ProductNotExistInList("Produto não encontrado na lista de favoritos.")

    product.delete()


def view_product_favorite(id_client: str, product_api: BaseApiProduct) -> list:
    list_product = Product.objects.filter(id_client=id_client)

    if len(list_product) == 0:
        return {}

    products = product_api.get_all_product(list_product)

    return products


class ClientDuplicate(Exception):
    pass


class ClientNotExist(Exception):
    pass


class ProductExistInList(Exception):
    pass


class ProductNotExistInList(Exception):
    pass


class ProductNotExist(Exception):
    pass
