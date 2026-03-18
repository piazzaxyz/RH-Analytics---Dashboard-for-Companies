from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class AbstractBuilder(ABC, Generic[T]):
    def __init__(self):
        self._instance = None
        self.reset()

    @abstractmethod
    def reset(self) -> None:
        """Reinicia o estado interno do builder"""
        ...

    @abstractmethod
    def build(self) -> T:
        """Retorna o objeto construído e chama reset()"""
        ...
