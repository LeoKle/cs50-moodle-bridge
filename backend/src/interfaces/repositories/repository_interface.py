from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")


class IRepository[T](ABC):
    """Generic repository interface for CRUD operations."""

    @abstractmethod
    def create(self, data: T) -> T:
        pass

    @abstractmethod
    def get(self, item_id: str) -> T | None:
        pass

    @abstractmethod
    def get_all(self) -> list[T]:
        pass

    @abstractmethod
    def update(self, item_id: str, data: T) -> T | None:
        pass

    @abstractmethod
    def delete(self, item_id: str) -> bool:
        pass
