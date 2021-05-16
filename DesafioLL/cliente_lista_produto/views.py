from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status, generics
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated, AllowAny

from . import domain
from .serializers import ClientSerializer, FavoriteSerializer, FavoriteViewSerializer, UserSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .integracao.product_api_challange import ProductChallengeApi
from .integracao.cache_product_redis import ProductRedisCache
import os
import logging

TTL_CACHE_MINUTE = os.environ.get("TTL_CACHE_MINUTE", None)
PAGE_SIZE_PRODUCT_DEFAULT = os.environ.get("PAGE_SIZE_PRODUCT_DEFAULT", 10)

product_redis_cache = ProductRedisCache(ttl=TTL_CACHE_MINUTE)
product_api = ProductChallengeApi(cache_product=product_redis_cache)

LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s -10s Function: %(funcName) "
    "-10s Line: %(lineno) -5d: %(message)s"
)
logging.basicConfig(format=LOG_FORMAT)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def client(request):
    if request.method == 'POST':
        client_data = JSONParser().parse(request)
        ciente_serializer = ClientSerializer(data=client_data)
        if ciente_serializer.is_valid():
            try:
                new_client = domain.register_client(ciente_serializer.data)
            except domain.ClientDuplicate as e:
                result = {"message": str(e)}
                return JsonResponse(result, status=status.HTTP_400_BAD_REQUEST, safe=False)
            except Exception as e:
                logging.critical(f"An exception with no specific handling was caught. Exception details: {str(e)}")
                result = {"message": f"Falha ao cadastrar cliente. Motivo: {str(e)}"}
                return JsonResponse(result, status=status.HTTP_400_BAD_REQUEST)

            result = {"id": new_client.id, "name": new_client.name, "email": new_client.email}
            return JsonResponse(result, status=status.HTTP_201_CREATED)

        return JsonResponse(ciente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET":
        try:
            clients = domain.view_all_client()
            client_serializer = ClientSerializer(clients, many=True)
            return JsonResponse(client_serializer.data, safe=False)
        except Exception as e:
            logging.critical(f"An exception with no specific handling was caught. Exception details: {str(e)}")
            result = {"message": f"Falha ao visualizar clientes. Motivo: {str(e)}"}
            return JsonResponse(result, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def client_detail(request, id_client):
    if request.method == 'GET':
        try:
            client_view = domain.view_client(id_client)
            client_serializer = ClientSerializer(client_view)
            return JsonResponse(client_serializer.data, status=status.HTTP_200_OK)
        except domain.ClientNotExist as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logging.critical(f"An exception with no specific handling was caught. Exception details: {str(e)}")
            result = {"message": f"Falha ao atualizar cliente. Motivo: {str(e)}"}
            return JsonResponse(result, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        client_data = JSONParser().parse(request)
        client_serializer = ClientSerializer(data=client_data)
        if client_serializer.is_valid():
            try:
                domain.change_client(id_client, client_serializer.data)
                return JsonResponse(client_serializer.data, status=status.HTTP_200_OK)
            except domain.ClientDuplicate as e:
                return JsonResponse({"message": str(e)}, status=status.HTTP_409_CONFLICT)
            except domain.ClientNotExist as e:
                return JsonResponse({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                logging.critical(f"An exception with no specific handling was caught. Exception details: {str(e)}")
                result = {"message": f"Falha ao atualizar cliente. Motivo: {str(e)}"}
                return JsonResponse(result, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try:
            domain.remove_client(id_client)
            return JsonResponse({'message': 'Cliente removido com sucesso'}, status=status.HTTP_200_OK)
        except domain.ClientNotExist as e:
            return JsonResponse({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logging.critical(f"An exception with no specific handling was caught. Exception details: {str(e)}")
            result = {"message": f"Falha ao remover cliente. Motivo: {str(e)}"}
            return JsonResponse(result, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'DELETE', 'GET'])
@permission_classes([IsAuthenticated])
def client_favorite(request, id_client=None):
    if request.method == 'POST':
        favorite_data = JSONParser().parse(request)
        try:
            product = domain.add_product_to_list_favorite_client(
                id_client=id_client,
                id_product=favorite_data["id_product"],
                product_api=product_api
            )
            product_serializer = FavoriteSerializer(product)
            return JsonResponse(product_serializer.data, status=status.HTTP_201_CREATED)
        except domain.ClientNotExist as e:
            return JsonResponse({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except domain.ProductNotExist as e:
            return JsonResponse({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except domain.ProductExistInList as e:
            return JsonResponse({"message": str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            logging.critical(f"An exception with no specific handling was caught. Exception details: {str(e)}")
            result = {"message": f"Falha ao adicionar o produto aos favoritos. Motivo: {str(e)}"}
            return JsonResponse(result, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        favorite_data = JSONParser().parse(request)
        try:
            domain.remove_product_favorite(id_product=favorite_data["id_product"], id_client=id_client)
            return JsonResponse({'message': 'Produto removido com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except domain.ClientNotExist as e:
            return JsonResponse({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except domain.ProductNotExist as e:
            return JsonResponse({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except domain.ProductNotExistInList as e:
            return JsonResponse({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logging.critical(f"An exception with no specific handling was caught. Exception details: {str(e)}")
            result = {"message": f"Falha ao remover produto dos favoritos. Motivo: {str(e)}"}
            return JsonResponse(result, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        try:
            page_size = PAGE_SIZE_PRODUCT_DEFAULT
            products = domain.view_product_favorite(id_client, product_api)
            paginator = Paginator(products, page_size)
            page = request.GET.get("page")
            product_page = paginator.get_page(page)

            data = {
                "meta": {
                    "page_size": page_size,
                    "page_number": product_page.number,
                    "num_pages": paginator.num_pages
                 },
                "product_favorite": product_page.object_list
             }

            return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except domain.ClientNotExist as e:
            return JsonResponse({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logging.critical(f"An exception with no specific handling was caught. Exception details: {str(e)}")
            result = {"message": f"Falha ao obter produto dos favoritos. Motivo: {str(e)}"}
            return JsonResponse(result, status=status.HTTP_400_BAD_REQUEST)


class CreateUser(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
