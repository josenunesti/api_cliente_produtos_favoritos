import abc


class BaseApiProduct(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_all_product(self, list_product: list) -> list:
        pass

    @abc.abstractmethod
    def get_product(self, id_product: str) -> dict:
        pass

    @abc.abstractmethod
    def exist_product(self, id_product) -> bool:
        pass


class BaseCacheProduct(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_product(self, id_product: str) -> dict:
        pass

    @abc.abstractmethod
    def set_product(self, product: dict) -> None:
        pass
