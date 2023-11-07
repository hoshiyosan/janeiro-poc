from abc import ABC, abstractmethod


class ConfigLoader(ABC):
    @abstractmethod
    def get(self, key: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def raise_missing_key(self, key: str):
        raise NotImplementedError
